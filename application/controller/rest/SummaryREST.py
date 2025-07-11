from application.models.automation.date_setter.DateSetterLastMonthToday import DateSetterLastMonthToday
from application.models.automation.date_setter.DateSetterCurrentMonth import DateSetterCurrentMonth
from application.models.automation.date_setter.DateSetterLastMonth import DateSetterLastMonth
from application.service.SummaryService import SummaryService
from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv 
from decouple import config  
from datetime import datetime
from logging.handlers import RotatingFileHandler
from  application.persistence.SummaryDAO import SummaryDAO
import logging 
import os 

load_dotenv()  # para cargar el .env en local

class SummaryREST:

    def __init__(self):
        self.app = Flask(__name__, template_folder="../../../front/templates", static_folder="../../../front/static")
        self.initialize_logging()
        self.setup_routes()
        self.month_and_year = f"{datetime.now().month}-{datetime.now().year}"
        self.service = SummaryService()

    def initialize_logging(self):
        handler = RotatingFileHandler('summary_api.log', maxBytes=5000000, backupCount=3)
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[handler]
        )

    #endpoints
    def setup_routes(self):
        # carga la pagina principal con sus datos
        @self.app.route("/hola", methods=["GET"])
        def hola():
            return jsonify({"respuesta":"hola"}), 200
        
        @self.app.route("/", methods=["GET"])
        def index():
            data1 = self.service.get_json(self.month_and_year)
            return render_template("index.html", data1=data1)
        
        @self.app.route("/json", methods=["GET"])
        def summary_json():
            return self.service.get_json(self.month_and_year)

        @self.app.route("/find_or_create", methods=["GET"])
        def find_or_create():
            data1 = self.service.find_or_create(self.month_and_year)
            return jsonify({"data": "se encontro"}), 200
        
        # actualiza el resumen al ultimo hecho
        @self.app.route("/resumenActual", methods=["PUT"])
        def update_summary():
            try:
                json = (self.service.update_by_date_setter(self.month_and_year, DateSetterCurrentMonth(None))), 200
                print(json)
                return jsonify(json)
            except Exception as e:
                logging.error(f"Error al actualizar el resumen: {e}")
                print(f"Error al actualizar el resumen: {e}")
                return jsonify({"message": f"Error al actualizar: {e}"}), 500
        
        # actualiza el resumen de este mismo dia pero de un mes atras 
        @self.app.route("/resumenDeUnMesAtras", methods=["PUT"])
        def update_total_last_months_total_today():
            try:
                json = (self.service.update_by_date_setter(self.month_and_year, DateSetterLastMonthToday(None))), 200
                print(json)
                return jsonify(json)
            except Exception as e:
                logging.error(f"Error al actualizar el resumen: {e}")
                print(f"Error al actualizar el resumen: {e} {e.__traceback__} {type(e)}")
                return jsonify({"message": f"Error al actualizar: {e}"}), 500
            
        # actualiza el resumen del total obtenido en todo el mes anterior 
        @self.app.route("/resumenDelMesPasado", methods=["PUT"])
        def update_total_last_months_total():
            try:
                json = (self.service.update_by_date_setter(self.month_and_year, DateSetterLastMonth(None))), 200
                print(json)
                return jsonify(json)
            except Exception as e:
                logging.error(f"Error al actualizar el resumen: {e}")
                print(f"Error al actualizar el resumen: {e}")
                return jsonify({"message": f"Error al actualizar: {e}"}), 500
        
    def run(self):
        port = int(os.environ.get("PORT", 5000))  # Railway Port = 5000 | Render Port = 10000
        print(f"Application is running at http://0.0.0.0:{port}")
        self.app.run(host="0.0.0.0", port=port, debug=False, use_reloader=True)

if __name__ == "__main__":
    try:
        app_routes = SummaryREST()
        app_routes.run()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
