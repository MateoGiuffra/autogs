import json
from firebase_admin import credentials, initialize_app, firestore
from decouple import config

DB_KEY = config("DB_KEY")

cred_data = json.loads(DB_KEY)

cred = credentials.Certificate(cred_data)
initialize_app(cred)

db = firestore.client()
