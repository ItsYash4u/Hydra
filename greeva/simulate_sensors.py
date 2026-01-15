import time
import random
import json
import urllib.request
import urllib.error
from datetime import datetime

API_URL = "http://127.0.0.1:8000/api/devices/sensors/ingest/"
DEVICE_ID = "DEV-SIMULATOR-001"

def generate_payload():
    base_temp = 24.0
    return {
        "device_id": DEVICE_ID,
        "temperature": round(base_temp + random.uniform(-2, 2), 2),
        "humidity": round(60 + random.uniform(-10, 10), 1),
        "ph": round(6.0 + random.uniform(-0.5, 0.5), 2),
        "ec": round(1.5 + random.uniform(-0.2, 0.2), 2),
        "tds": round(750 + random.uniform(-50, 50), 0),
        "co2": random.randint(400, 800),
        "light": round(random.uniform(10, 16), 1),
        "water_temp": round(22 + random.uniform(-1, 1), 2),
        "dissolved_oxygen": round(random.uniform(5, 8), 1)
    }

def main():
    print(f"Starting Sensor Simulator for Device: {DEVICE_ID}")
    print(f"Target URL: {API_URL}")
    print("Press Ctrl+C to stop.")
    
    while True:
        try:
            payload = generate_payload()
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(API_URL, data=data, headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Sensor-Simulator/1.0'
            })
            
            with urllib.request.urlopen(req) as response:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Sent: Temp={payload['temperature']}C Ph={payload['ph']} [Status: {response.getcode()}]")
                
        except urllib.error.URLError as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Error: {e}")
            if hasattr(e, 'read'):
                print(e.read().decode())
        except Exception as e:
             print(f"Error: {e}")
            
        time.sleep(5)

if __name__ == "__main__":
    main()
