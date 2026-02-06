import sys
print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version}")
try:
    import environ
    print("SUCCESS: environ module found.")
    print(f"environ file: {environ.__file__}")
except ImportError as e:
    print(f"ERROR: environ module NOT found. {e}")

try:
    import PIL
    print("SUCCESS: PIL (Pillow) module found.")
    print(f"PIL file: {PIL.__file__}")
except ImportError as e:
    print(f"ERROR: PIL module NOT found. {e}")
