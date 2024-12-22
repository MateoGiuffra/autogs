from decouple import config  
from application.automation.WebDriverManager import WebDriverManager
from application.pandas.ExcelReader import ExcelReader
from AbsPath import AbsPath

import logging

class SummaryService:
    BASE_URL = "https://game.systemmaster.com.ar/frmLogin.aspx"
    DB_USER = config("DB_USER")
    DB_PASSWORD = config("DB_PASSWORD")
    LAST_TOTAL = 0
    TOTAL =  0
    WEB_DRIVER_MANAGER = WebDriverManager(AbsPath.obtener_abspath(),'rptCobranzas*.xls' )

    def __init__(self):
        self.initialize_logging() 

    def initialize_logging(self):
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='webdriver_errors.log',
            filemode='a'
        )

    @staticmethod
    def get_summary(cache_manager):
        cached_summary = cache_manager.get_cached_data()
        if cached_summary:
            return SummaryService.answer_totals(cached_summary)

        try:
            total = SummaryService.get_total()
            SummaryService.set_totals(total)
            cache_manager.update_cache(total)
            return SummaryService.answer_totals(total)
        except Exception as e:
            logging.error(f"Error al obtener el resumen: {e}")
            raise     
    
    def set_totals(new_total):
        if  SummaryService.LAST_TOTAL == 0 and SummaryService.TOTAL == 0:  SummaryService.TOTAL = new_total
        if  SummaryService.TOTAL != 0:
            SummaryService.LAST_TOTAL = SummaryService.TOTAL 
            SummaryService.TOTAL = new_total
       

    def answer_totals(new_total):
        return f"El total actual es: {new_total}. Se obtuvieron {new_total - SummaryService.LAST_TOTAL} pesos más que la anterior vez."
    
    def get_total():
        SummaryService.WEB_DRIVER_MANAGER.start(SummaryService.BASE_URL, SummaryService.DB_USER, SummaryService.DB_PASSWORD)

        path = SummaryService.WEB_DRIVER_MANAGER.get_downloaded_file_path()
        excel_reader = ExcelReader(path)

        return float(excel_reader.get_total())

   

