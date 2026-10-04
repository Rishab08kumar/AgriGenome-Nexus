import firebase_admin
from firebase_admin import credentials, db, firestore
from .config import settings

_app = None

def get_firebase_app():
    global _app
    if not _app:
        try:
            if settings.FIREBASE_CREDENTIALS_PATH:
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                options = {}
                if settings.FIREBASE_DATABASE_URL:
                    options['databaseURL'] = settings.FIREBASE_DATABASE_URL
                if settings.FIREBASE_PROJECT_ID:
                    options['projectId'] = settings.FIREBASE_PROJECT_ID
                _app = firebase_admin.initialize_app(cred, options)
            else:
                _app = firebase_admin.initialize_app()
        except Exception as e:
            print("Firebase init error:", e)
    return _app

def get_db():
    get_firebase_app()
    return db

def get_firestore():
    get_firebase_app()
    return firestore.client()

def push_sensor_data(data: dict):
    try:
        ref = get_db().reference('sensor_data')
        ref.push(data)
        return True
    except Exception as e:
        print("Error pushing sensor data:", e)
        return False

def get_latest_sensor_data():
    try:
        ref = get_db().reference('sensor_data')
        latest = ref.order_by_key().limit_to_last(1).get()
        if latest:
            for key, val in latest.items():
                return val
        return None
    except Exception as e:
        print("Error getting latest sensor data:", e)
        return None
