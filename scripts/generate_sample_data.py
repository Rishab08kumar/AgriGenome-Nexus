import firebase_admin
from firebase_admin import credentials, db
import random
import math
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

def initialize_firebase():
    cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH', '../firebase-credentials.json')
    database_url = os.getenv('FIREBASE_DATABASE_URL')
    
    if not database_url:
        print("Please set FIREBASE_DATABASE_URL in .env")
        return None
        
    try:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': database_url
        })
        return db.reference('sensor_history')
    except Exception as e:
        print(f"Firebase Init Error: {e}")
        return None

def generate_historical_data(num_records=1000, days_back=30):
    data = {}
    now = datetime.utcnow()
    
    for i in range(num_records):
        # Calculate timestamp going back 30 days
        dt = now - timedelta(days=days_back * (num_records - i) / num_records)
        hour = dt.hour
        
        # Realistic cycles
        temp_base = 22 + 16 * math.sin(math.pi * (hour - 6) / 12) if 6 <= hour <= 18 else 22 + 5 * math.sin(math.pi * (hour + 6) / 12)
        temp = max(22, min(38, temp_base + random.uniform(-2, 2)))
        
        light_base = 100000 * math.sin(math.pi * (hour - 6) / 12) if 6 <= hour <= 18 else 0
        light = max(0, light_base + random.uniform(-10000, 10000))
        
        record = {
            "timestamp": dt.isoformat(),
            "soil_moisture": max(10, min(90, 50 + 20 * math.sin(i / 100) + random.uniform(-5, 5))),
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
        
        # Use timestamp as key
        key = dt.strftime("%Y%m%d%H%M%S") + str(i % 1000).zfill(3)
        data[key] = record
        
    return data

def main():
    print("Generating 1000 historical records...")
    data = generate_historical_data(1000, 30)
    
    print("Initializing Firebase...")
    ref = initialize_firebase()
    if not ref:
        return
        
    print("Uploading to Firebase in batches...")
    # Push to firebase in one large update for efficiency
    try:
        ref.update(data)
        print("Upload complete!")
    except Exception as e:
        print(f"Upload failed: {e}")

if __name__ == "__main__":
    main()
