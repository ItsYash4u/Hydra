import subprocess
import sys

def check():
    print("Running check...")
    try:
        subprocess.check_call([sys.executable, "manage.py", "check"])
        print("Check passed")
    except subprocess.CalledProcessError as e:
        print(f"Check failed: {e}")

if __name__ == "__main__":
    check()
