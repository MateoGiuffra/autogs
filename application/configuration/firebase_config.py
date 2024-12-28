import json
from firebase_admin import credentials, initialize_app, firestore
from decouple import config
import os 
# Leer la clave JSON directamente desde el .env
# DB_KEY = config("DB_KEY")

cred_data = {
        "type": "service_account",
        "project_id": config("DB_PROJECT_ID"),
        "private_key_id": config("DB_PRIVATE_KEY_ID"),
        "private_key": config("DB_PRIVATE_KEY").replace("\\n", "\n"),
        "client_email": config("DB_CLIENT_EMAIL"),
        "client_id": config("DB_CLIENT_ID"),
        "auth_uri": config("DB_AUTH_URI"),
        "token_uri": config("DB_TOKEN_URI"),
        "auth_provider_x509_cert_url": config("DB_AUTH_PROVIDER_CERT_URL"),
        "client_x509_cert_url": config("DB_CLIENT_CERT_URL"),
        "universe_domain": "googleapis.com"
    }
# Convertir la cadena JSON en un diccionario
# cred_data = json.loads(DB_KEY)

# Usar los datos para inicializar la aplicación Firebase
cred = credentials.Certificate(cred_data)
initialize_app(cred)

# Instancia de Firestore
db = firestore.client()
