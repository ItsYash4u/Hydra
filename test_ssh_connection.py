import subprocess
import os

def test_ssh():
    pem_file = "hydroponics_sys.pem"
    ip = "54.173.213.113"
    user = "ubuntu"
    
    print(f"Testing SSH to {user}@{ip} using {pem_file}")
    
    # Simple check for file existence
    if not os.path.exists(pem_file):
        print(f"Error: {pem_file} not found")
        return

    # Verbose SSH command
    cmd = [
        "ssh", "-i", pem_file,
        "-v",
        "-o", "ConnectTimeout=10",
        "-o", "BatchMode=yes",
        "-o", "StrictHostKeyChecking=no",
        f"{user}@{ip}",
        "echo 'Verified'"
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(timeout=15)
        
        print(f"Exit Code: {process.returncode}")
        print("--- STDOUT ---")
        print(stdout)
        print("--- STDERR ---")
        print(stderr)
        
    except subprocess.TimeoutExpired:
        print("SSH command timed out after 15 seconds")
        process.kill()
        stdout, stderr = process.communicate()
        print("--- STDOUT (captured before timeout) ---")
        print(stdout)
        print("--- STDERR (captured before timeout) ---")
        print(stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    test_ssh()
