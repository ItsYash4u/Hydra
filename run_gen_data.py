import subprocess
import sys

def run():
    print("Running generate_data...")
    try:
        subprocess.check_call([sys.executable, "manage.py", "generate_data"])
        print("Successfully generated data")
    except subprocess.CalledProcessError as e:
        print(f"Failed to generate data: {e}")

if __name__ == "__main__":
    run()
