import logging
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
from decouple import config

# Configuración de constantes
TIMEZONE = config("TIMEZONE", default="America/Argentina/Buenos_Aires")
API_BASE_URL = config("API_BASE_URL", default="http://127.0.0.1:10000")

class SchedulerService:
    def __init__(self):
        self.scheduler = BackgroundScheduler(timezone=timezone(TIMEZONE))

    def start(self):
        """
        Inicia el scheduler y maneja posibles errores de inicio.
        """
        try:
            self.scheduler.start()
            logging.info(f"Scheduler iniciado con éxito. Horario de {TIMEZONE}")
        except Exception as e:
            logging.error(f"Error al iniciar el Scheduler: {e}")
    
    def scheduler_jobs(self):
        """
        Configura los trabajos del scheduler, evitando duplicados.
        """
        try:
            if not self.scheduler.get_job("update_summary_daily"):
                self.scheduler.add_job(
                    func=self.call_resumenDeUnMesAtras,
                    trigger='cron',
                    minute='*/3',  # Cada 3 minutos
                    id="update_summary_daily",
                    replace_existing=True
                )
                logging.info("Job 'update_summary_daily' configurado correctamente.")
            
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
                logging.info("Job 'update_summary_monthly' configurado correctamente.")
        except Exception as e:
            logging.error(f"Error al configurar los trabajos del Scheduler: {e}")

    @staticmethod
    def call_resumenDeUnMesAtras():
        """
        Llama al endpoint `/resumenDeUnMesAtras` y maneja los posibles errores.
        """
        url = f"{API_BASE_URL}/resumenDeUnMesAtras"
        logging.info(f"Llamando al endpoint: {url}")
        try:
            response = requests.put(url, timeout=10)  # Timeout para evitar bloqueos
            if response.status_code == 200:
                logging.info("Resumen de este mismo día pero un mes atrás actualizado correctamente.")
            else:
                logging.warning(f"Error en el endpoint '/resumenDeUnMesAtras'. "
                                f"Status code: {response.status_code}, "
                                f"Response: {response.text}")
        except requests.ConnectionError as e:
            logging.error(f"Error de conexión al ejecutar '/resumenDeUnMesAtras': {e}")
        except requests.Timeout as e:
            logging.error(f"Timeout al ejecutar '/resumenDeUnMesAtras': {e}")
        except Exception as e:
            logging.error(f"Error general al ejecutar '/resumenDeUnMesAtras': {e}")

    @staticmethod
    def call_resumenDelMesPasado():
        """
        Llama al endpoint `/resumenDelMesPasado` y maneja los posibles errores.
        """
        url = f"{API_BASE_URL}/resumenDelMesPasado"
        logging.info(f"Llamando al endpoint: {url}")
        try:
            response = requests.put(url, timeout=10)  # Timeout para evitar bloqueos
            if response.status_code == 200:
                logging.info("Resumen del mes pasado actualizado correctamente.")
            else:
                logging.warning(f"Error en el endpoint '/resumenDelMesPasado'. "
                                f"Status code: {response.status_code}, "
                                f"Response: {response.text}")
        except requests.ConnectionError as e:
            logging.error(f"Error de conexión al ejecutar '/resumenDelMesPasado': {e}")
        except requests.Timeout as e:
            logging.error(f"Timeout al ejecutar '/resumenDelMesPasado': {e}")
        except Exception as e:
            logging.error(f"Error general al ejecutar '/resumenDelMesPasado': {e}")
