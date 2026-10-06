import os
import firebase_admin
from firebase_admin import credentials, firestore

db = None

try:
    if not firebase_admin._apps:
        # Check for credential file or environment variables
        cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase_creds.json")
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            print("🔥 Firebase initialized successfully using service account file!")
        else:
            # Initialize default app if running in cloud/mock mode
            firebase_admin.initialize_app()
            db = firestore.client()
            print("🔥 Firebase initialized in default mode!")
except Exception as e:
    print(f"⚠️ Firebase initialization skipped or failed: {e}. Falling back to in-memory/mock database.")
    db = None

def push_sensor_data(data: dict):
    if db is not None:
        try:
            db.collection("sensor_data").add(data)
            return True
        except Exception as err:
            print(f"Error pushing to Firebase: {err}")
    return False

def get_latest_sensor_data():
    if db is not None:
        try:
            docs = db.collection("sensor_data").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(1).get()
            for doc in docs:
                return doc.to_dict()
        except Exception as err:
            print(f"Error fetching from Firebase: {err}")
    
    # In-memory baseline fallback if Firebase is not connected
    return {
        "soil_moisture": 62.5,
        "humidity": 68.0,
        "temperature": 24.5,
        "light_intensity": 45000,
        "ec": 1.2,
        "ph": 6.4,
        "note": "Baseline Telemetry Mode"
    }