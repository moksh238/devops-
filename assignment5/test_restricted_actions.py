
import docker

client = docker.from_env()

test_code = r'''
import subprocess

print("AppArmor label:", open("/proc/self/attr/current").read().strip())

# Test reading /etc/passwd
try:
    with open("/etc/passwd", "r") as file:
        file.read()
    print("Attempt to read /etc/passwd: ALLOWED (unexpected)")
except PermissionError as error:
    print(f"Attempt to read /etc/passwd: BLOCKED ({error})")

# Test executing /bin/bash
try:
    result = subprocess.run(
        ["/bin/bash", "-c", "echo bash-executed"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("Attempt to execute /bin/bash: ALLOWED (unexpected)")
    else:
        print(
            f"Attempt to execute /bin/bash: FAILED "
            f"(exit code {result.returncode})"
        )
        print(result.stderr.strip())

except PermissionError as error:
    print(f"Attempt to execute /bin/bash: BLOCKED ({error})")
'''

print("Starting restricted-action tests...")

output = client.containers.run(
    "flask-apparmor",
    entrypoint="/usr/local/bin/python",
    command=["-c", test_code],
    security_opt=["apparmor=my-apparmor-profile"],
    remove=True
)

print(output.decode("utf-8", errors="replace"))
print("Restricted-action tests completed.")

