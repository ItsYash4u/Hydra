
import subprocess
import sys

def run_migrations():
    print("Running makemigrations...")
    # Add 'y' just in case of prompts
    cmd = [sys.executable, "manage.py", "makemigrations", "hydroponics", "--name", "fix_sensor_fk"]
    
    try:
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=r"c:\Users\AYUSH\OneDrive\Desktop\noone\Hydroponics\Greeva\greeva")
        stdout, stderr = process.communicate(input="y\n")
        
        print("STDOUT:\n", stdout)
        print("STDERR:\n", stderr)
        
        if process.returncode == 0:
            print("Running migrate...")
            cmd_mig = [sys.executable, "manage.py", "migrate"]
            process_mig = subprocess.Popen(cmd_mig, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=r"c:\Users\AYUSH\OneDrive\Desktop\noone\Hydroponics\Greeva\greeva")
            out_mig, err_mig = process_mig.communicate()
            print("MIGRATE STDOUT:\n", out_mig)
            print("MIGRATE STDERR:\n", err_mig)
        else:
            print("Makemigrations failed.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_migrations()
