import subprocess
import sys

def run_migration():
    print("Running migration and capturing output...")
    try:
        # Run migrate
        result = subprocess.run(
            [sys.executable, 'manage.py', 'migrate'],
            capture_output=True,
            text=True
        )
        print("--- STDOUT ---")
        print(result.stdout)
        print("--- STDERR ---")
        print(result.stderr)
        
        if result.returncode == 0:
            print("Migration success!")
            # Run loaddata
            print("Running loaddata...")
            res_load = subprocess.run(
                [sys.executable, 'manage.py', 'loaddata', 'datadump.json'],
                capture_output=True,
                text=True
            )
            print("--- LOAD STDOUT ---")
            print(res_load.stdout)
            print("--- LOAD STDERR ---")
            print(res_load.stderr)
        else:
            print("Migration failed.")
            
    except Exception as e:
        print(f"Execution Error: {e}")

if __name__ == "__main__":
    run_migration()
