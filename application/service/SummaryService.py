from decouple import config  
from application.automation.date_setter.DateSetterCurrentMonth import DateSetterCurrentMonth
from application.automation.date_setter.DateSetterLastMonth import DateSetterLastMonth
from application.automation.WebDriverManager import WebDriverManager
from application.pandas.ExcelReader import ExcelReader
from AbsPath import AbsPath
import threading
from application.service.utils.CacheManager import CacheManager

import logging

class SummaryService:
    BASE_URL = "https://game.systemmaster.com.ar/frmLogin.aspx"
    DB_USER = config("DB_USER")
    DB_PASSWORD = config("DB_PASSWORD")

    def __init__(self):
        self.web_driver_manager = WebDriverManager(AbsPath.obtener_abspath(), 'rptCobranzas*.xls')
        self.initialize_logging()
        self.lock = threading.Lock()

    def initialize_logging(self):
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='webdriver_errors.log',
            filemode='a'
        )

    def get_summary(self):
        try:
            total = self.get_total(DateSetterCurrentMonth(None))
            return self.answer(total)
        except Exception as e:
            logging.error(f"Error al obtener el resumen: {e}")
            raise

    def dif_summaries(self, total):
        try:
            last_month_total = self.get_total(DateSetterLastMonth(None))
            return {
                "message": self.calculate_dif(last_month_total, total),
                "last_month_total": last_month_total
            } 
        except Exception as e:
            logging.error(f"Error al obtener el resumen: {e}")
            raise
    
    def answer(self, total):
        message = f"El total actual es: {total}"
        return {
                "total": total,
                "message": message
               }
      
    def calculate_dif(self, last_month_total, current_total):
        try:
            dif = current_total - last_month_total
            porcent = (dif / last_month_total) * 100
            return(
                   f"El mes pasado se llegó a los: {last_month_total} de pesos. " 
                   f"Por lo tanto, actualmente hay un {porcent:.2f}% mas que el mes anterior. Habiendo una diferencia de {abs(dif):.2f} de pesos entre ambos."
            ) 
        except ZeroDivisionError:
            print("Error: No se puede dividir por 0")
            return f"El monto total del mes pasado fue de $ 0."
        except Exception as e:
            print(f"Error inesperado en calculate_dif: {e}") 
            return 
        
    def get_total(self, type_date):
        self.web_driver_manager.set_date_setter(type_date)
        self.web_driver_manager.start(self.BASE_URL, self.DB_USER, self.DB_PASSWORD)
        
        path = self.web_driver_manager.get_downloaded_file_path()
        
        excel_reader = ExcelReader(path)
        total =  float(excel_reader.get_total())
        print("Se obtuvo el total con exito: " + str(total))
        return total

        
