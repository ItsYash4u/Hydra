import subprocess
import sys

def run(cmd):
    print(f"Running: {cmd}")
    try:
        # Using input='y\n' to auto-answer yes if prompted, though risky
        result = subprocess.run(
            cmd, shell=True, 
            capture_output=True, 
            text=True,
            input="1\n1\n" # providing defaults if asked '1' then '1' (e.g. select option 1, then value 1)
        )
        print("RC:", result.returncode)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        with open("migration_log.txt", "a", encoding='utf-8') as f:
            f.write(f"\nCMD: {cmd}\n")
            f.write(f"RC: {result.returncode}\n")
            f.write(result.stdout)
            f.write(result.stderr)
    except Exception as e:
        print(e)
        with open("migration_log.txt", "a", encoding='utf-8') as f:
            f.write(f"\nERROR: {e}\n")

if __name__ == "__main__":
    run("python manage.py makemigrations users")
    run("python manage.py makemigrations hydroponics")
    run("python manage.py migrate")
