from decouple import config  
from application.automation.WebDriverManager import WebDriverManager
from application.pandas.ExcelReader import ExcelReader
from abs_path import dir
import logging
class Summary:

    BASE_URL = "https://game.systemmaster.com.ar/frmLogin.aspx"
    DB_USER = config("DB_USER")
    DB_PASSWORD = config("DB_PASSWORD")
    
    def __init__(self, month_and_year):
        self.web_driver_manager = WebDriverManager(dir, 'rptCobranzas*.xls')
        self.initialize_logging()
        self.total = 0
        self.last_total  = 0
        self.last_months_total = 0
        self.last_months_total_today = 0
        self.month_and_year = month_and_year
    
    def initialize_logging(self):
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='summary.log',
            filemode='a'
        )

    def get_total_number(self, date_setter):
        self.web_driver_manager.set_date_setter(date_setter)
        self.web_driver_manager.start(self.BASE_URL, self.DB_USER, self.DB_PASSWORD)
        
        path = self.web_driver_manager.get_downloaded_file_path()
        
        excel_reader = ExcelReader(path)
        total =  float(excel_reader.get_total())
        
        date_setter.set_summary_total(self, total)

        print(f"Se obtuvo el total con exito: {total}")
        print(f"Se settearon con exito en Summary el total: {self.total} y el last_total: {self.last_total}")

        return total
    
    def answer_of_current_total(self):
        if self.last_total:
            return {
                "message": f"El total actual es: {self.total} de pesos. Se obtuvieron {self.total - self.last_total} pesos más que la anterior vez.",
                "total": f"{self.total}"
            }
        return {
                "message": f"El total actual es: {self.total} de pesos.",
                "total": f"{self.total}"
            }

    def calculate_dif(self, last_month_total, current_total):
        try:
            self.validate_current_total(current_total)
            dif = current_total - last_month_total
            porcent = (dif / last_month_total) * 100
            more_or_less = "menos" if dif < 0 else "mas" 
            return {
                     "message" : (
                         f"El mes pasado se llegó a los: {last_month_total} de pesos. " 
                         f"Por lo tanto, actualmente hay un {abs(porcent):.2f}% {more_or_less} que el mes anterior. Habiendo una diferencia de {abs(dif):.2f} de pesos entre ambos."
                     ),
                     "last_month_total": last_month_total
                   }
        except ZeroDivisionError:
            print("Error: No se puede dividir por 0")
            return {
                     "message": f"El monto total del mes pasado fue de $ 0.",
                     "last_month_total": 0
                   }
        except Exception as e:
            print(f"Error inesperado en calculate_dif: {e}") 
            raise 

    def validate_current_total(self, current_total):
        if current_total: return 
        raise Exception("Antes de comparar resumenes primero se tiene que obtener resumen del dia")
    
   # getters  
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
    def set_total(self, total):
        self.total = total 
    
    def set_last_total(self, last_total):
        self.last_total = last_total

    def set_last_months_total(self, last_months_total):
        self.last_months_total = last_months_total   
        
    def set_last_months_total_today(self, last_months_total_today):
        self.last_months_total_today = last_months_total_today         
        
    

        

        