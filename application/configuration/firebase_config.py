import sys
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(project_dir, "..", ".."))
sys.path.append(project_root)
from AbsPath import AbsPath
from firebase_admin import credentials, initialize_app, firestore

# Ruta al archivo de credenciales
KEY_PATH =  AbsPath.get_key_abspath()

# Inicialización de Firebase
cred = credentials.Certificate(KEY_PATH)
initialize_app(cred)

# Instancia del cliente Firestore
db = firestore.client()
