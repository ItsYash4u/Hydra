import requests
import sys

def check_api():
    url = "http://127.0.0.1:8001/hydroponics/api/devices/"
    try:
        response = requests.get(url, auth=('admin@example.com', 'password'))
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Response JSON:")
            print(response.json())
        else:
            print("Failed to fetch data")
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_api()
