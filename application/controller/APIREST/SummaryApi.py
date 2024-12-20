from application.controller.utils.CacheManager import CacheManager
from application.service.SummaryService import SummaryService
from flask import Flask, jsonify, request
from dotenv import load_dotenv 
from decouple import config  
import logging 
import os 

load_dotenv()  # para cargar el .env en local

class SummaryApi:
    BASE_URL = "https://game.systemmaster.com.ar/frmLogin.aspx"
    DB_USER = config("DB_USER")
    DB_PASSWORD = config("DB_PASSWORD")
    CACHE_TIMEOUT = 10 * 60
    TOTAL = 0

    def __init__(self):
        self.app = Flask(__name__)
        self.cache_manager = CacheManager(SummaryApi.CACHE_TIMEOUT)     
        self.initialize_logging()   
        self.setup_routes()

    def initialize_logging(self):
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='webdriver_errors.log',
            filemode='a'
        )

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
            except ValueError | Exception as ve:
                response_message = str(ve)
                return self.answer_message(response_message, 400)
    
    def validate_incoming_message(self, incoming_message):
        if (incoming_message != "resumen"): 
             raise ValueError("Mensaje no reconocido. Envía 'resumen' para obtener el total. Si no proba entrando al link: https://autogs-2.onrender.com/obtenerResumen")

    def get_summary(self):
        cached_summary = self.cache_manager.get_cached_data()
        if cached_summary:
            return cached_summary

        try:
            total = SummaryService.get_summary(SummaryApi.BASE_URL, SummaryApi.DB_USER, SummaryApi.DB_PASSWORD)
            self.cache_manager.update_cache(total)
            return total
        except Exception as e:
            logging.error(f"Error al obtener el resumen: {e}")
            raise e
    
    def set_new_total(self):
        pass
        # current_time = time.time()
        # time_since_last_summary = current_time - SummaryApi.cache["timestamp"]
        # # si fue pedido hace menos de 10 minutos no hace nada
        # if SummaryApi.cache["summary"] is not None and  time_since_last_summary < SummaryApi.CACHE_TIMEOUT: return
        # # caso contrario, calcula
        # SummaryApi.total = SummaryService.get_summary(SummaryApi.BASE_URL, SummaryApi.DB_USER, SummaryApi.DB_PASSWORD)
        # SummaryApi.cache["summary"] =  SummaryApi.total 
        # SummaryApi.cache["timestamp"] = current_time 
    
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
