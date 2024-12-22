from application.service.utils.CacheManager import CacheManager
from application.service.SummaryService import SummaryService
from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv 
from decouple import config  
import logging 
import os 

load_dotenv()  # para cargar el .env en local

class SummaryApi:

    TIMEOUT = 10 * 60
    CACHE = CacheManager(10 * 60) 

    def __init__(self):
        self.app = Flask(__name__, template_folder="../../../front/templates",  static_folder='static')
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
        # @self.app.route("/", methods=["GET"])
        # def index():
        #     return render_template("index.html")
    
        @self.app.route("/test", methods=["GET"])
        def test():
            return "Prueba exitosa", 200
        
        @self.app.route("/obtenerResumen", methods=["GET"])
        def get_summary():
            try:
               return jsonify(SummaryService.get_summary(SummaryApi.CACHE)), 200
            except Exception as p:
                print()
                return jsonify("Hubo un error, intentalo mas tarde:" +  str(p)), 500
         
        @self.app.route("/diferenciaResumenes", methods=["GET"])
        def dif_summaries():
            try:
               return jsonify(SummaryService.dif_summaries(SummaryApi.CACHE)), 200
            except Exception as p:
                print()
                return jsonify("Hubo un error, intentalo mas tarde:" +  str(p)), 500

        @self.app.route("/resumen", methods=["POST"])
        def send_summary():
            incoming_message = request.form.get("Body", "").strip().lower()
            try:
                self.validate_incoming_message(incoming_message)
                response_message = SummaryService.SERVICE.get_summary()
                return self.answer_message(response_message, 200)
            except ValueError | Exception as ve:
                response_message = str(ve)
                return self.answer_message(response_message, 400)
    
    def validate_incoming_message(self, incoming_message):
        if (incoming_message != "resumen"): 
             print("no es un mensaje valido")
             raise ValueError("Mensaje no reconocido. Envía 'resumen' para obtener el total. Si no proba entrando al link: https://autogs-2.onrender.com/obtenerResumen")
    
    def answer_message(self, message, value):
        response = f"""<Response>
                         <Message>{message}</Message>
                    </Response>"""
        return response, value, {'Content-Type': 'application/xml'}   

    def run(self):
        port = int(os.environ.get("PORT", 10000))
        self.app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)


if __name__ == "__main__":
    try:
        app_routes = SummaryApi()
        app_routes.run()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
