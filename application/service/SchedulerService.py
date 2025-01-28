from application.models.automation.date_setter.DateSetterLastMonthToday import DateSetterLastMonthToday
from application.models.automation.date_setter.DateSetterLastMonthToday import DateSetterLastMonth
from apscheduler.schedulers.background import BackgroundScheduler
from application.service.SummaryService import SummaryService
from datetime import datetime
from decouple import config
from pytz import timezone
import requests
import logging

# Configuración de constantes
TIMEZONE = config("TIMEZONE", default="America/Argentina/Buenos_Aires")
API_BASE_URL = config("API_BASE_URL", default="http://127.0.0.1:10000")

class SchedulerService:
    MONTH_AND_YEAR = f"{datetime.now().month}-{datetime.now().year}"
    def __init__(self):
        self.scheduler = BackgroundScheduler(timezone=timezone(TIMEZONE))
        

    def start(self):
        try:
            self.scheduler.start()
            logging.info(f"Scheduler iniciado con éxito. Horario de {TIMEZONE}")
        except Exception as e:
            logging.error(f"Error al iniciar el Scheduler: {e}")
    
    def scheduler_jobs(self):
        try:
            if not self.scheduler.get_job("update_summary_daily"):
                self.scheduler.add_job(
                    func=self.call_resumenDeUnMesAtras,
                    trigger='cron',
                    hour=1,
                    minute=0, 
                    id="update_summary_daily",
                    replace_existing=True
                )
                logging.info("Job 'update_summary_daily' configured correctly.")
            
            if not self.scheduler.get_job("update_summary_monthly"):
                self.scheduler.add_job(
                    func=self.call_resumenDelMesPasado,
                    trigger='cron',
                    day=1,
                    hour=0,
                    minute=5,
                    id="update_summary_monthly",
                    replace_existing=True
                )
                logging.info("Job 'update_summary_monthly' configured correctly.")
            if not self.scheduler.get_job("keep_active"):
                self.scheduler.add_job(
                    func=self.keep_active,
                    trigger='interval',
                    minutes=5, 
                    id="keep_active",
                    replace_existing=True
                )
                logging.info("Job 'keep_active' configured correctly to execute every 5 minutes.")
        except Exception as e:
            logging.error(f"Error in Scheduler Jobs configuration: {e}")

    @staticmethod
    def call_resumenDeUnMesAtras():
        logging.info(f"Dentro de call_resumenDeUnMesAtras")
        try:
            service = SummaryService()
            service.update_by_date_setter(SchedulerService.MONTH_AND_YEAR, DateSetterLastMonthToday(None)) 
            logging.info("resumen de un mes atras bien hecho") 
            print("resumen de un mes atras bien hecho") 
        except requests.ConnectionError as e:
            logging.error(f"Error de conexión al ejecutar call_resumenDeUnMesAtras: {e}")
        except requests.Timeout as e:
            logging.error(f"Timeout al ejecutar call_resumenDeUnMesAtras: {e}")
        except Exception as e:
            logging.error(f"Error general al ejecutar call_resumenDeUnMesAtras: {e}")

    @staticmethod
    def call_resumenDelMesPasado():
        logging.info(f"Dentro de call_resumenDelMesPasado")
        try:
            service = SummaryService()
            service.update_by_date_setter(SchedulerService.MONTH_AND_YEAR, DateSetterLastMonth(None)) 
            logging.info("resumen de un mes atras bien hecho") 
            print("resumen de un mes atras bien hecho") 
        except requests.ConnectionError as e:
            logging.error(f"Error de conexión al ejecutar call_resumenDelMesPasado: {e}")
        except requests.Timeout as e:
            logging.error(f"Timeout al ejecutar call_resumenDelMesPasado: {e}")
        except Exception as e:
            logging.error(f"Error general al ejecutar call_resumenDelMesPasado: {e}")

    @staticmethod
    def keep_active():
        url = "https://www.google.com"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("Successful request to Google.")
            else:
                print(f"Google request error : {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error to connection: {e}")