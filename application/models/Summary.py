from application.models.automation.WebDriverManager import WebDriverManager
from application.models.pandas.excel_reader import reader_get_total
from datetime import datetime
from zoneinfo import ZoneInfo 
from decouple import config  
from abs_path import dir
import logging
import pytz 

TIMEZONE = config("TIMEZONE", default="America/Argentina/Buenos_Aires")
class Summary:

    BASE_URL = "https://game.systemmaster.com.ar/frmLogin.aspx"
    DB_USER = config("DB_USER")
    DB_PASSWORD = config("DB_PASSWORD")
    
    def __init__(self, month_and_year):
        try: 
            self.web_driver_manager = WebDriverManager(dir, 'rptCobranzas*.xls')
            self.initialize_logging()
            self.month_and_year = month_and_year
            self.total = 0
            self.last_total  = 0
            self.last_months_total = 0
            self.last_months_total_today = 0
            self.last_report_date = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires")).strftime("%d-%m-%Y %H:%M:%S")
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
        
        return total
    
    # devuelve un JSON con la informacion del objeto
    def to_summary_dict(self):
        return {
            "total": self.total,  
            "last_total": self.last_total,  
            "last_months_total": self.last_months_total,   
            "last_months_total_today": self.last_months_total_today, 
            "last_report_date" : self.last_report_date
        }
    
    @classmethod
    def from_dict(cls, month_and_year, data):
        instance = cls(month_and_year)
        instance.total = float(data.get("total", 0))
        instance.last_total = float(data.get("last_total", 0))
        instance.last_months_total = float(data.get("last_months_total", 0))
        instance.last_months_total_today = float(data.get("last_months_total_today", 0))
        instance.last_report_date = data.get("last_report_date", datetime.now(pytz.timezone("America/Argentina/Buenos_Aires")).strftime("%d-%m-%Y %H:%M:%S"))
        return instance
    
   # getters  
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
        
    

        

        