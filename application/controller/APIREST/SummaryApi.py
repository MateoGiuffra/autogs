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
        self.total = 0
        self.last_month_total = 0

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
        
        @self.app.route("/diferenciaResumenes", methods=["GET"])
        def dif_summaries():
            try: 
                print("El total actual es de: " + str(self.total))
                service = SummaryService()
                if self.last_month_total != 0: 
                    service.calculate_dif(self.last_month_total, self.total) 
                answerJSON = service.dif_summaries(self.total)
                self.last_month_total =  answerJSON["last_month_total"] 
                return jsonify(answerJSON["message"]),200
            except Exception as e:
                print(str(e))
                return jsonify("Hubo un error, intentalo mas tarde:" +  str(e)), 500

        @self.app.route("/obtenerResumen", methods=["GET"])
        def get_summary():
            try:
                service = SummaryService()
                answerJSON = service.get_summary()
                self.total = answerJSON["total"]
                print("Se guardo el total " + str(answerJSON["total"]) + " en la API: " + str(self.total))
                return jsonify(answerJSON["message"]), 200
            except Exception as p:
                print()
                return jsonify("Hubo un error, intentalo mas tarde: " +  str(p)), 500
         
    def run(self):
        port = int(os.environ.get("PORT", 10000))
        self.app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)


if __name__ == "__main__":
    try:
        app_routes = SummaryApi()
        app_routes.run()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
