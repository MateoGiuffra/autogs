from decouple import config  
from application.automation.WebDriverManager import WebDriverManager
from abs_path import dir
import logging
from datetime import datetime
from application.pandas.excel_reader import reader_get_total
import pytz 
from zoneinfo import ZoneInfo 

TIMEZONE = config("TIMEZONE", default="America/Argentina/Buenos_Aires")
class Summary:

    BASE_URL = "https://game.systemmaster.com.ar/frmLogin.aspx"
    DB_USER = config("DB_USER")
    DB_PASSWORD = config("DB_PASSWORD")
    
    def __init__(self, month_and_year):
        try: 
            self.web_driver_manager = WebDriverManager(dir, 'rptCobranzas*.xls')
            self.initialize_logging()
            self.total = 0
            self.last_total  = 0
            self.last_months_total = 0
            self.last_months_total_today = 0
            self.month_and_year = month_and_year
            self.last_report_date = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires")).strftime("%d-%m-%Y %H:%M:%S")
            print(f"Aca esta la fecha de mierda {self.last_report_date} ")
            self.message_last_months_total = "Todavia no se calculo ninguna diferencia"
            self.message_last_months_total_today = "Todavia no se calculo ninguna diferencia"
        except Exception as e: 
            message = f"Error al inicializar instancia de Summary: {e}"
            print(message)
            raise Exception(message) 
         
    
    def initialize_logging(self):
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='summary.log',
            filemode='a'
        )

    # Obtener el total de la fecha dada. Este metodo obtiene el excel, lo lee y settea los valores segun el tipo de fecha requerida. 
    def get_total_number(self, date_setter):
        self.web_driver_manager.set_date_setter(date_setter)
        self.web_driver_manager.start(self.BASE_URL, self.DB_USER, self.DB_PASSWORD)
        
        path = self.web_driver_manager.get_downloaded_file_path()
        
        total = float(reader_get_total(path))
        
        date_setter.update_info(self, total)

        print(f"Se obtuvo el total con exito: {total}")
        print(f"Se settearon con exito en Summary el total: {self.total} y el last_total: {self.last_total}")
        
        return total

    def calculate_dif(self, last_month_total, current_total):
        try:
            dif = current_total - last_month_total
            percent = (dif/last_month_total) * 100
            return self.percent_message(dif, percent, last_month_total)
        except ZeroDivisionError:
            print("Error: No se puede dividir por 0")
            return f"El monto total del mes pasado fue de $ 0."
        except Exception as e:
            print(f"Error inesperado en calculate_dif: {e}") 
            raise 
        
    def percent_message(self, dif, percent, last_month_total):
        more_or_less = "mas" if dif > 0 else "menos" 
        return ( f"El mes pasado se llegó a los: {last_month_total} de pesos. " 
                 f"Por lo tanto, actualmente hay un {abs(percent):.2f}% {more_or_less} que el mes anterior. Habiendo una diferencia de {abs(dif):.2f} de pesos entre ambos." ) 
        
    
    # devuelve un JSON con la informacion del objeto
    def to_summary_dict(self):
        return {
            "total": self.total,  
            "last_total": self.last_total,  
            "last_months_total": self.last_months_total,   
            "last_months_total_today": self.last_months_total_today, 
            "last_report_date" : self.last_report_date, 
            "message_last_months_total" : self.message_last_months_total, 
            "message_last_months_total_today" : self.message_last_months_total_today
        }
    
    @classmethod
    def from_dict(cls, month_and_year, data):
        instance = cls(month_and_year)
        instance.total = float(data.get("total", 0))
        instance.last_total = float(data.get("last_total", 0))
        instance.last_months_total = float(data.get("last_months_total", 0))
        instance.last_months_total_today = float(data.get("last_months_total_today", 0))
        instance.last_report_date = data.get("last_report_date", datetime.now(pytz.timezone("America/Argentina/Buenos_Aires")).strftime("%d-%m-%Y %H:%M:%S"))
        instance.message_last_months_total = data.get("message_last_months_total", {"message": "JSON vacio"})
        instance.message_last_months_total_today = data.get("message_last_months_total_today", {"message": "JSON vacio"})
        return instance
    
   # getters  
    def get_message_last_months_total(self):
        return self.message_last_months_total
    
    def get_message_last_months_total_today(self):
        return self.message_last_months_total_today
    
    def get_last_report_date(self):
        return self.last_report_date
   
    def get_total(self):
        return self.total 

    def get_last_total(self):
        return self.last_total

    def get_last_months_total(self):
        return self.last_months_total

    def get_last_months_total_today(self):
        return self.last_months_total_today
    
    def get_month_and_year(self):
        return self.month_and_year

    # setters  
    def set_message_last_months_total(self, json):
        self.message_last_months_total = json 
        
    def set_message_last_months_total_today(self, json):
        self.message_last_months_total_today = json 
    
    def set_last_report_date(self, date): 
        if (isinstance(date, str)):
             self.last_report_date = date 
             return 
        self.last_report_date = date.strftime("%d-%m-%Y %H:%M:%S")
    
    def set_total(self, total):
        self.total = total 
    
    def set_last_total(self, last_total):
        self.last_total = last_total

    def set_last_months_total(self, last_months_total):
        self.last_months_total = last_months_total   
        
    def set_last_months_total_today(self, last_months_total_today):
        self.last_months_total_today = last_months_total_today         
        
    

        

        