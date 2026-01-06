import os
try:
    os.remove("greeva/hydroponics/migrations/0001_initial.py")
    print("Deleted 0001_initial.py")
except FileNotFoundError:
    print("File not found")
except Exception as e:
    print(f"Error: {e}")
