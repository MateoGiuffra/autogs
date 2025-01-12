from firebase_admin import credentials, initialize_app, firestore
from decouple import config
import json
#inicializa una unica instancia de firestore para comunicarse con la base de datos
DB_KEY = config("DB_KEY")

cred_data = json.loads(DB_KEY)

cred = credentials.Certificate(cred_data)
initialize_app(cred)

db = firestore.client()
