import sys
try:
    import pymysql
    print("pymysql: installed")
    print(f"pymysql version: {pymysql.__version__}")
except ImportError:
    print("pymysql: not installed")

try:
    import django
    print("django: installed")
    print(f"django version: {django.get_version()}")
except ImportError:
    print("django: not installed")

print(f"Python executable: {sys.executable}")
