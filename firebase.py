import os
import firebase_admin
from firebase_admin import credentials, firestore, storage
from dotenv import load_dotenv

load_dotenv()

service_account_key_path = os.getenv('GOOGLE_CLOUD_SERVICE_ACCOUNT')

cred = credentials.Certificate('./firebase-adminsdk.json')

default_app = firebase_admin.initialize_app(cred, {
    'storageBucket': 'brss-8827a.firebasestorage.app'
})

db = firestore.client()
bucket = storage.bucket()
