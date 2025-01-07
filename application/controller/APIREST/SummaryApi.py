from application.service.SummaryService import SummaryService
from application.automation.date_setter.DateSetterLastMonth import DateSetterLastMonth
from application.automation.Summary import Summary
from application.automation.date_setter.DateSetterCurrentMonth import DateSetterCurrentMonth
from application.automation.date_setter.DateSetterLastMonthToday import DateSetterLastMonthToday
from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv 
from decouple import config  
from datetime import datetime
import logging 
import os 

load_dotenv()  # para cargar el .env en local

class SummaryApi:

    def __init__(self):
        self.app = Flask(__name__, template_folder="../../../front/templates", static_folder="../../../front/static")
        self.initialize_logging()   
        self.setup_routes()
        self.month_and_year = f"{datetime.now().month}-{datetime.now().year}"

    def initialize_logging(self):
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='summary_api.log',
            filemode='a'
        )
    #endpoints
    def setup_routes(self):
        # carga la pagina principal con sus datos
        @self.app.route("/", methods=["GET"])
        def index():
            service = SummaryService()
            data1 = service.get_info(self.month_and_year)
            print(f"aca esta {data1}")    
            return render_template("pagina.html", data1=data1)
        
        # actualiza el resumen al ultimo hecho
        @self.app.route("/actualizar_resumen", methods=["PUT"])
        def update_summary():
            service = SummaryService()
            service.update_total()

        #endpoints innecesarios
        @self.app.route("/obtenerResumen", methods=["GET"])
        def get_summary():
            try:
                service = SummaryService()
                answerJSON = service.get_summarys_answer(DateSetterCurrentMonth(None), self.month_and_year)
                print("El total del answerJSON de la API es: " + str(answerJSON["total"]))
                return jsonify(answerJSON), 200 
            except Exception as p:
                answerJSON =  {"message": f"Hubo un error, intentalo mas tarde: {p}"}
                return jsonify(answerJSON), 500

        @self.app.route("/diferenciaResumenes", methods=["GET"])
        def diferencia_resumenes():
            print("Se le pegó al endpoint diferenciaResumenes")
            return self.dif_summaries(DateSetterLastMonth(None))

        @self.app.route("/diferenciaResumenesHoy", methods=["GET"])
        def diferencia_resumenes_hoy():
            print("Se le pegó al endpoint diferenciaResumenesHoy")
            return self.dif_summaries(DateSetterLastMonthToday(None))
    

    def dif_summaries(self, date_setter):
        try: 
            service = SummaryService()
            answerJSON =  service.dif_summaries(date_setter, self.month_and_year)
            return jsonify(answerJSON), 200
        except Exception as e: 
            answerJSON = {"message": "Hubo un error, intentalo mas tarde:" +  str(e)}
            return jsonify(answerJSON), 500               

    def run(self):
        port = int(os.environ.get("PORT", 10000))
        self.app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)


if __name__ == "__main__":
    try:
        app_routes = SummaryApi()
        app_routes.run()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
