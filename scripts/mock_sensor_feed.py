import time
import json
import random
import requests
import math
from datetime import datetime

API_URL = "http://localhost:8000/api/sensor-data"

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def generate_sensor_data(time_offset):
    hour = (time.localtime().tm_hour + time_offset) % 24
    
    # Simulate daily cycles
    temp_base = 22 + 16 * math.sin(math.pi * (hour - 6) / 12) if 6 <= hour <= 18 else 22 + 5 * math.sin(math.pi * (hour + 6) / 12)
    temp = max(22, min(38, temp_base + random.uniform(-1, 1)))
    
    light_base = 100000 * math.sin(math.pi * (hour - 6) / 12) if 6 <= hour <= 18 else 0
    light = max(0, light_base + random.uniform(-5000, 5000))
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "soil_moisture": random.uniform(20.0, 80.0),
        "humidity": random.uniform(50.0, 90.0),
        "temperature": temp,
        "light_intensity": light,
        "nitrogen": random.uniform(150.0, 350.0),
        "phosphorus": random.uniform(20.0, 80.0),
        "potassium": random.uniform(100.0, 300.0),
        "ec": random.uniform(0.5, 3.0),
        "ph": None,
        "weight": None
    }

def main():
    print(f"{Colors.HEADER}Starting mock sensor feed to {API_URL}...{Colors.ENDC}")
    time_offset = 0
    while True:
        try:
            data = generate_sensor_data(time_offset)
            time_offset += 0.1 # Slow drift over time
            
            response = requests.post(API_URL, json=data)
            
            if response.status_code == 200:
                print(f"{Colors.OKGREEN}[{datetime.now().strftime('%H:%M:%S')}] Success:{Colors.ENDC}")
                print(json.dumps(data, indent=2))
            else:
                print(f"{Colors.FAIL}[{datetime.now().strftime('%H:%M:%S')}] Failed ({response.status_code}): {response.text}{Colors.ENDC}")
                
        except requests.exceptions.ConnectionError:
            print(f"{Colors.WARNING}[{datetime.now().strftime('%H:%M:%S')}] Connection failed. Backend down?{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}[{datetime.now().strftime('%H:%M:%S')}] Error: {str(e)}{Colors.ENDC}")
            
        time.sleep(5)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.HEADER}Stopping mock sensor feed.{Colors.ENDC}")
