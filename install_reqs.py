import subprocess
import sys

def install():
    print("Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements/local.txt"])
        print("Successfully installed requirements")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install requirements: {e}")

if __name__ == "__main__":
    install()
