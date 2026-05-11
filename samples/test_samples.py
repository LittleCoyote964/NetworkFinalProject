import subprocess
import urllib.request
import time

#What this does is:
#Create a file
#modifies or appends to a file
#runs a child process
#attempts a network request
#sleeps briefly before finishing

print("Sample started....")

with open("/sandbox/sandbox_arena/created_file.txt", "w") as file:
    file.write("This file was created by the test sample.\n")

with open("/sandbox/sandbox_arena/activity_log.txt", "a") as file:
    file.write("The sample modified this log file.\n")

subprocess.run(["echo", "Child process executed"])

try:
    urllib.request.urlopen("http://example.com", timeout=3)
except Exception as e:
    print("Network request failed or was blocked.", e)

time.sleep(2)

print("Sample finished.")