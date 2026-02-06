import requests
import sys

try:
    print("Checking specific pages...")
    
    # 1. Dashboard
    resp = requests.get("http://127.0.0.1:8000/", timeout=5)
    print(f"Dashboard: {resp.status_code}")
    
    # 2. Login Page
    resp = requests.get("http://127.0.0.1:8000/accounts/login/", timeout=5)
    print(f"Login Page: {resp.status_code}")

    if resp.status_code == 200:
        print("SUCCESS: Website is running.")
    else:
        print("WARNING: Website returned non-200 code.")
        
except Exception as e:
    print(f"ERROR: Could not connect to server. {e}")
