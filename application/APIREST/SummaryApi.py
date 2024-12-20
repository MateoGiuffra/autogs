from flask import Flask, jsonify, request
from application.service.SummaryService import SummaryService
from decouple import config  
import os 
import time 
from dotenv import load_dotenv 
load_dotenv()  # para cargar el .env en local

class SummaryApi:
    BASE_URL = "https://game.systemmaster.com.ar/frmLogin.aspx"
    DB_USER = config("DB_USER")
    DB_PASSWORD = config("DB_PASSWORD")
    CACHE_TIMEOUT = 10 * 60
    TOTAL = 0
    cache = {
    "summary": None, 
    "timestamp":0 
    }

    def __init__(self):
        self.app = Flask(__name__)
        self.total = 0
        self.setup_routes()

    def setup_routes(self):
        @self.app.route("/obtenerResumen", methods=["GET"])
        def obtener_resumen():
            try:
                return jsonify(self.get_summary()), 200
            except Exception as e:
                error_message = {"error": str(e)}
                return jsonify(error_message), 500
        
        @self.app.route("/resumen", methods=["POST"])
        def recibir_mensaje():
            incoming_message = request.form.get("Body", "").strip().lower()
            try:
                self.validate_incoming_message(incoming_message)
                response_message = self.get_summary()
                return self.answer_message(response_message, 200)
            except ValueError as ve:
                return self.answer_message("Mensaje no reconocido. Envía 'resumen' para obtener el total. Si no proba entrando al link: https://autogs-2.onrender.com/obtenerResumen" , 400)
    
    def validate_incoming_message(self, incoming_message):
        if (incoming_message != "resumen"): 
             raise ValueError("Mensaje no reconocido. Envía 'resumen' para obtener el total. Si no proba entrando al link: https://autogs-2.onrender.com/obtenerResumen")

    def get_summary(self):
        try: 
            self.set_new_total()           
            return  f"El total es: {SummaryApi.total}"
        except Exception as e: 
            return f"Error: {str(e)}"
    
    def set_new_total(self):
        current_time = time.time()
        time_since_last_summary = current_time - SummaryApi.cache["timestamp"]
        # si fue pedido hace menos de 10 minutos no hace nada
        if SummaryApi.cache["summary"] is not None and  time_since_last_summary < SummaryApi.CACHE_TIMEOUT: return
        # caso contrario, calcula
        SummaryApi.total = SummaryService.get_summary(SummaryApi.BASE_URL, SummaryApi.DB_USER, SummaryApi.DB_PASSWORD)
        SummaryApi.cache["summary"] =  SummaryApi.total 
        SummaryApi.cache["timestamp"] = current_time 
    
    def answer_message(self, message, value):
        response = f"""<Response>
                         <Message>{message}</Message>
                    </Response>"""
        return response, value, {'Content-Type': 'application/xml'}   

    def run(self):
        port = int(os.environ.get("PORT", 10000))
        self.app.run(host="0.0.0.0", port=port, debug=True)

# Ejecutar la aplicación
if __name__ == "__main__":
    app_routes = SummaryApi()
    app_routes.run()
