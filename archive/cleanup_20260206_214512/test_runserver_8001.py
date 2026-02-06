import subprocess
import sys
import time

def run_server():
    print("Starting server on 8001...")
    proc = subprocess.Popen(
        [sys.executable, "manage.py", "runserver", "0.0.0.0:8001"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    try:
        # Wait a bit
        time.sleep(5)
        if proc.poll() is not None:
            print(f"Server exited early with code {proc.returncode}")
            print(proc.stdout.read())
        else:
            print("Server is running...")
            # Keep it running for a while to test
            time.sleep(10)
            # Kill it to read output
            proc.terminate()
            try:
                outs, _ = proc.communicate(timeout=5)
                print(outs)
            except subprocess.TimeoutExpired:
                proc.kill()
                outs, _ = proc.communicate()
                print(outs)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_server()
