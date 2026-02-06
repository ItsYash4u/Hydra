import subprocess
import sys
import os

def run_frontend():
    client_dir = os.path.join(os.getcwd(), 'client')
    print("Installing frontend dependencies...")
    try:
        subprocess.check_call(["npm", "install"], shell=True, cwd=client_dir)
        print("Dependencies installed.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        return

    print("Starting frontend server...")
    try:
        # Use shell=True for npm on Windows
        subprocess.Popen(["npm", "run", "dev"], shell=True, cwd=client_dir)
        print("Frontend server started.")
    except Exception as e:
        print(f"Failed to start frontend server: {e}")

if __name__ == "__main__":
    run_frontend()
