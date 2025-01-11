import logging 
import requests 
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone 
from decouple import config  

TIMEZONE = config("TIMEZONE", default="America/Argentina/Buenos_Aires")
API_BASE_URL= config("API_BASE_URL", default = "http://127.0.0.1:10000")

class SchedulerService():
    
    def __init__(self):
        self.scheduler = BackgroundScheduler(timezone=timezone(TIMEZONE))
        
    def start(self):
        try:
            self.scheduler.start()
            print(f"Scheduler iniciado con exite. Horario de {TIMEZONE}")
        except Exception as e: 
            logging.error(f"Error al iniciar el Scheduler: {e}")
    
    
    def scheduler_jobs(self):
        try: 
            if not self.scheduler.get_job("update_summary_daily"):
                # Job para el endpoint resumentDeUnMesAtras - Todos los dias a las 00:05
                self.scheduler.add_job(
                    func=self.call_resumenDeUnMesAtras, 
                    trigger='cron',
                    minute='*/3',
                    # hour= 11, 
                    # minute=57,
                    id="update_summary_daily",
                    replace_existing=True 
                )
            # Job para el endpoint resumenDelMesPasado  - Primer día de cada mes a las 00:05
            if not self.scheduler.get_job("update_summary_monthly"):
                self.scheduler.add_job(
                    self.call_resumenDelMesPasado,
                    "cron",
                    day=1,
                    hour=0,
                    minute=5,
                    id="update_summary_monthly",
                    replace_existing=True
                )
        except Exception as e: 
            print(f"Ocurrio un error al configurar el scheduler: {e}")
            logging.error(f"Error al programar trabajos en el Scheduler: {e}")
            
        
    @staticmethod
    def call_resumenDeUnMesAtras():
        try: 
            url = f"https://vivacious-playfulness-production.up.railway.app/resumenDeUnMesAtras"
            print(f"Aca esta la url que le esta pegando {url}")
            request = requests.put(url)
            if request.status_code == 200: 
                print("Resumen de este mismo dia pero un mes atras actualizado")
            else: 
                print("No se recibio un 200 al hacer el put de resumenDeUnMesAtras")
        except request.ConnectionError as e: 
            message = f"Error de conexion al ejecutar resumenDeUnMesAtras {e}"
            print(message)
            logging.error(message)
        except Exception as e: 
            message = f"Error general al ejecutar resumenDeUnMesAtras {e}"
            print(message)
            logging.error(message)
            
    @staticmethod
    def call_resumenDelMesPasado():
        try: 
            request = requests.put(f"{API_BASE_URL}/resumenDelMesPasado")
            if request.status_code == 200: 
                print("Resumen de este mismo dia pero un mes atras actualizado")
            else: 
                print("No se recibio un 200 al hacer el put de resumenDelMesPasado")
        except request.ConnectionError as e: 
            message = f"Error de conexion al ejecutar resumenDelMesPasado {e}"
            print(message)
            logging.error(message)
        except Exception as e: 
            message = f"Error general al ejecutar resumenDelMesPasado {e}"
            print(message)
            logging.error(message)