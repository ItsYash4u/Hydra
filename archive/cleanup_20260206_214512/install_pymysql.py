import subprocess
import sys

def install():
    print("Installing pymysql...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pymysql"])
        print("Successfully installed pymysql")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install pymysql: {e}")

if __name__ == "__main__":
    install()
