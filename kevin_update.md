## Kevin Update for Nick
### I think I got it to work..? 

Everything seems to be working. The sanbox successfully: 
* Executed the sample
* Generated a behavioral report
* Logged filesystem changes
* Captured stdout/stderr
* Recorded syscall traces with strace

The outputs should confirm that the framework is functioning as intended. 

## How To Run
### Requirements

Before running the project, install: 
- Docker
Verify Docker is installed: 

```bash
docker --version
```

---

### Build the Docker Image

From the root project directory, build the container: 

```bash
docker build -t sandbox-analyzer
```

This creates a Docker image named: 

```text
sandbox-analyzer
```

---

### Run the Container

Start the sandbox container interactively:

```bash
docker run -it sandbox-analyzer
```

You should now be inside the container:

```text
root@container-id:/sandbox#
```

---

### Run the Sample

Execute the sandbox runner against the provided sample:

```bash
python3 sandbox_runner.py samples/test_samples.py
```

Expected output:

```text
[+] Analyzing sample: /sandbox/samples/test_samples.py
[+] SHA256: <hash>
[+] Running sample with strace...
[+] Analysis complete.
[+] Report has been saved to: /sandbox/report/analysis_report.txt
```

---

### View the Analysis Report

List the contents of the report directory:

```bash
ls -la report
```

Open the generated report:

```bash
cat report/analysis_report.txt
```

Example output:

```text
Sandbox Malware Analysis Report
========================================

Sample Path: /sandbox/samples/test_samples.py

Created Files:
   - /sandbox/sandbox_area/activity_log.txt
   - /sandbox/sandbox_area/created_file.txt
```

---

## View Logs

List generated logs:

```bash
ls -la logs
```

### Process Output Log

```bash
cat logs/process.log
```

Example:

```text
STDOUT:
Child process executed
Sample started....
Sample finished.
```

---

### File Change Log

```bash
cat logs/file_changes.json
```

Example:

```json
{
    "created": [
        "/sandbox/sandbox_area/activity_log.txt",
        "/sandbox/sandbox_area/created_file.txt"
    ],
    "deleted": [],
    "modified": []
}
```

---

### System Call Trace

View the first few captured system calls:

```bash
head -40 logs/syscalls.log
```

Search for networking activity:

```bash
grep connect logs/syscalls.log
```