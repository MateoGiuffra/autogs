from application.service.utils.CacheManager import CacheManager
from application.service.SummaryService import SummaryService
from application.automation.date_setter.DateSetterLastMonth import DateSetterLastMonth
from application.automation.date_setter.DateSetterLastMonthToday import DateSetterLastMonthToday
from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv 
from decouple import config  
import logging 
import os 

load_dotenv()  # para cargar el .env en local

class SummaryApi:

    TIMEOUT = 10 * 60

    def __init__(self):
        self.app = Flask(__name__, template_folder="../../../front/templates", static_folder="../../../front/static")
        self.initialize_logging()   
        self.setup_routes()
        self.total = 0
        self.last_month_total = 0
        self.last_month_total_today = 0
        self.cache = CacheManager(SummaryApi.TIMEOUT) 

    def initialize_logging(self):
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='webdriver_errors.log',
            filemode='a'
        )

    def setup_routes(self):
        @self.app.route("/", methods=["GET"])
        def index():
            return render_template("index.html")
        
        @self.app.route("/obtenerResumen", methods=["GET"])
        def get_summary():
            try:
                if (not self.cache.is_summary_zero()) and self.cache.didnt_arrive_at_established_time():
                    print("Respuesta de cache.")
                    answerJSON = self.cache.get_message()
                    return jsonify(answerJSON), 200 
                service = SummaryService()
                answerJSON = service.get_summary()
                self.total = answerJSON["total"]
                self.cache.update_cache(self.total)
                print("Se guardo el total " + str(answerJSON["total"]) + " en la API: " + str(self.total))
                return jsonify(answerJSON), 200 
            except Exception as p:
                answerJSON =  {"message": "Hubo un error, intentalo mas tarde: " +  str(p)}
                jsonify(answerJSON), 500

        @self.app.route("/diferenciaResumenes", methods=["GET"])
        def diferencia_resumenes():
            print("Se le pegó al endpoint diferenciaResumenes")
            try: 
                answerJSON = self.dif_summaries(DateSetterLastMonth(None), self.last_month_total)
                self.last_month_total =  answerJSON["last_month_total"] 
                return jsonify(answerJSON), 200 
            except Exception as e: 
                answerJSON = {"message": "Hubo un error, intentalo mas tarde:" +  str(e)}
                return jsonify(answerJSON), 500

        @self.app.route("/diferenciaResumenesHoy", methods=["GET"])
        def diferencia_resumenes_hoy():
            print("Se le pegó al endpoint diferenciaResumenesHoy")
            try: 
                answerJSON = self.dif_summaries(DateSetterLastMonthToday(None), self.last_month_total_today)
                self.last_month_total_today =  answerJSON["last_month_total"] 
                return jsonify(answerJSON), 200 
            except Exception as e: 
                answerJSON = {"message": "Hubo un error, intentalo mas tarde:" +  str(e)}
                return jsonify(answerJSON), 500
         
    def dif_summaries(self, date_setter, last_month):
            try: 
                print(f"El total actual es de: {self.total}")
                service = SummaryService()
                if last_month != 0: 
                    return service.calculate_dif(last_month, self.total)
                return service.dif_summaries(self.total, date_setter)
            except Exception as e:
                print(f"{e}")
                raise 
            
    def run(self):
        port = int(os.environ.get("PORT", 10000))
        self.app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)


if __name__ == "__main__":
    try:
        app_routes = SummaryApi()
        app_routes.run()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
