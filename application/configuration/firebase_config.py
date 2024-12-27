import json
from firebase_admin import credentials, initialize_app, firestore
from decouple import config

# Leer la clave JSON directamente desde el .env
DB_KEY = config("DB_KEY")

# Convertir la cadena JSON en un diccionario
cred_data = json.loads(DB_KEY)

# Usar los datos para inicializar la aplicación Firebase
cred = credentials.Certificate(cred_data)
initialize_app(cred)

# Instancia de Firestore
db = firestore.client()
