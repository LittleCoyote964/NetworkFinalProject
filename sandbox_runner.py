import os
import sys
import json
import hashlib
import subprocess
from pathlib import PATH

SANBOX_DIR = Path("/sandbox/sandbox_arena")
LOGS_DIR = Path("/sandbox/logs")
REPORTS_DIR = Path("/sandbox/reports")

SYSCALL_LOG = LOGS_DIR / "syscalls.log"
PROCESS_LOG = LOGS_DIR / "process.log"
FILE_CHANGE_LOG = LOGS_DIR / "file_changes.json"
REPORT_FILE = REPORTS_DIR / "analysis_report.txt"

def calculate_hash(file_path):
    """Calculate SHA256 hash of the sample."""
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()

def snapshot_files(directory):
    #record files before and after execution
    snapshot = {}

    for root, dir, files in os.walk(directory):
        for names in files:
            path = Path(root) / names

            try:
                snapshot[str(path)] = {
                    "size": path.stat().st_size,
                    "modified": path.stat().st_mtime
                }
            except FileNotFoundError:
                pass
    return snapshot

def compare_snapshots(before, after):
    """Compare snapshots and find created, deleted, and modified files"""
    before_files = set(before.keys())
    after_files = set(after.keys())

    created = sorted(list(after_files - before_files))
    deleted = sorted(list(before_files - after_files))

    modified = []

    for file_path in before_files & after_files:
        if before[file_path] != after[file_path]:
            modified.append(file_path)
    
    return {
        "created": created,
        "deleted": deleted,
        "modified": sorted(modified)
    }

def run_samples(sample_path):
    #what this would do is run the sample inside the sandbox using strace. 
    sample_path = Path(sample_path)

    if not sample_path.exists():
        print(f"[ERROR] Sample not found: {sample_path}")
        sys.exit(1)
    
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    SANBOX_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[+] Analyzing sample: {sample_path}")

    sample_hash = calculate_hash(sample_path)
    print(f"[+] SHA256: {sample_hash}")

    before_snapshot = snapshot_files(SANDBOX_DIR)

    command = [
        "strace",
        "-f",
        "-o",
        str(SYSCALL_LOG),
        "python3",
        str(sample_path)
    ]

    print("[+] Running sample with strace...")


    try: 
        result = subprocess.run(
            command,
            cwd=SANDBOX_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )

        with open(PROCESS_LOG, "w") as log:
            log.write("STDOUT:\n")
            log.write(result.stdout)
            log.write("\n\nSTFDERR:\n")
            log.write(result.stderr)
        
        except subprocess.TimeoutExpired:
            with open(PROCESS_LOG, "w") as log:
                log.write("Process timed out after 10 seconds.\n")
            
            print("[!] Sample timed out and was stopped.")

        after_snapshot = snapshot_files(SANDBOX_DIR)
        file_changes = compare_snapshots(before_snapshot, after_snapshot)

        with open(FILE_CHANGE_LOG, "w") as file:
            json.dump(file_changes, file, indent=4)
        
        generate_report(sample_path, sample_hash, file_changes)

        print(f"[+] Analysis complete.")
        print(f"[+] Report has been saved to: {REPORT_FILE}")

        