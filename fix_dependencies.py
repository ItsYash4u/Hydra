
import subprocess
import sys
import os

def install(package):
    print(f"Installing {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Installed {package}")
    except Exception as e:
        print(f"Failed to install {package}: {e}")

packages = [
    "django-environ",
    "django-allauth",
    "argon2-cffi",
    "whitenoise",
    "django-crispy-forms",
    "crispy-bootstrap5",
    "django-filter",
    "djangorestframework",
    "django-cors-headers"
]

log_file = "fix_deps_log.txt"

with open(log_file, "w") as f:
    f.write("Starting dependency fix...\n")

for p in packages:
    try:
        install(p)
        with open(log_file, "a") as f:
            f.write(f"Installed {p}\n")
    except:
        with open(log_file, "a") as f:
            f.write(f"Failed {p}\n")

print("Dependencies checks done.")

# Now try to import and run clean setup
try:
    import setup_project
    setup_project.setup()
    with open(log_file, "a") as f:
        f.write("Setup project ran successfully.\n")
except Exception as e:
    with open(log_file, "a") as f:
        f.write(f"Setup project failed: {e}\n")
