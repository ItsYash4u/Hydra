import os
from pathlib import Path

base = Path(os.getcwd())
target = base / "greeva" / "hydroponics" / "migrations" / "0001_initial.py"
print(f"Target: {target}")
if target.exists():
    try:
        target.unlink()
        print("Deleted.")
    except Exception as e:
        print(f"Error: {e}")
else:
    print("Not found.")
