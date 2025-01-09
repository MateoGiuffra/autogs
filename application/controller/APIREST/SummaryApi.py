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
from logging.handlers import RotatingFileHandler
from application.service.SchedulerService import SchedulerService

load_dotenv()  # para cargar el .env en local


class SummaryApi:

    def __init__(self):
        self.app = Flask(__name__, template_folder="../../../front/templates", static_folder="../../../front/static")
        self.initialize_logging()
        self.setup_routes()
        self.month_and_year = f"{datetime.now().month}-{datetime.now().year}"
        self.scheduler = SchedulerService()
        self.scheduler.scheduler_jobs()
        self.scheduler.start()

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
        @self.app.route("/", methods=["GET"])
        def index():
            service = SummaryService()
            data1 = service.get_info(self.month_and_year)
            print(f"aca esta {data1}")    
            return render_template("index.html", data1=data1)
        
        # actualiza el resumen al ultimo hecho
        @self.app.route("/resumenActual", methods=["PUT"])
        def update_summary():
            try:
                service = SummaryService()
                service.update_by_date_setter(self.month_and_year, DateSetterCurrentMonth(None))  
                summary = service.find_or_create(self.month_and_year)
                return jsonify(summary.get_info()), 200
            except Exception as e:
                logging.error(f"Error al actualizar el resumen: {e}")
                return jsonify({"message": f"Error al actualizar: {e}"}), 500

        # actualiza el resumen de este mismo dia pero de un mes atras 
        @self.app.route("/resumenDeUnMesAtras", methods=["PUT"])
        def update_total_last_months_total_today():
            try:
                service = SummaryService()
                service.update_by_date_setter(self.month_and_year, DateSetterLastMonthToday(None))  
                return jsonify({"message": "Resumen de un mes atras actualizado correctamente."}), 200
            except Exception as e:
                logging.error(f"Error al actualizar el resumen: {e}")
                return jsonify({"message": f"Error al actualizar: {e}"}), 500
            
        # actualiza el resumen del total obtenido en todo el mes anterior 
        @self.app.route("/resumenDelMesPasado", methods=["PUT"])
        def update_total_last_months_total():
            try:
                service = SummaryService()
                service.update_by_date_setter(self.month_and_year, DateSetterLastMonth(None)) 
                return jsonify({"message": "Resumen del mes pasado actualizado correctamente."}), 200
            except Exception as e:
                logging.error(f"Error al actualizar el resumen: {e}")
                return jsonify({"message": f"Error al actualizar: {e}"}), 500
        

    def run(self):
        port = int(os.environ.get("PORT", 10000))
        self.app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)


if __name__ == "__main__":
    try:
        app_routes = SummaryApi()
        app_routes.run()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
