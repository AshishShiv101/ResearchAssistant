import firebase_admin
from firebase_admin import credentials, firestore, storage
from app.core.config import settings
import os

# Ensure key file exists
if not os.path.exists(settings.firebase_key_path):
    raise FileNotFoundError(
        f"Firebase key not found at {settings.firebase_key_path}. "
        "Download it from Firebase Console → Project Settings → Service Accounts."
    )

# Initialize Firebase App (singleton)
cred = credentials.Certificate(settings.firebase_key_path)

# Only initialize once (important for FastAPI reloads)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        "storageBucket": f"{settings.project_id}.appspot.com"
    })

# Firestore client
db = firestore.client()

# Storage bucket
bucket = storage.bucket()

def get_firestore():
    """Return Firestore DB client"""
    return db

def get_bucket():
    """Return Firebase Storage bucket"""
    return bucket
