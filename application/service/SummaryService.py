from decouple import config  
from application.automation.date_setter.DateSetterCurrentMonth import DateSetterCurrentMonth
from application.automation.date_setter.DateSetterLastMonth import DateSetterLastMonth
from application.automation.WebDriverManager import WebDriverManager
from application.pandas.ExcelReader import ExcelReader
from AbsPath import AbsPath
import threading

import logging

class SummaryService:
    BASE_URL = "https://game.systemmaster.com.ar/frmLogin.aspx"
    DB_USER = config("DB_USER")
    DB_PASSWORD = config("DB_PASSWORD")

    def __init__(self):
        self.LAST_MONTH_TOTAL = None
        self.LAST_TOTAL = 0
        self.TOTAL = 0
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

    def get_summary(self, cache_manager):
        cached_summary = cache_manager.get_cached_data()
        if cached_summary:
            return self.answer_totals(cached_summary)

        try:
            total = self.get_total(DateSetterCurrentMonth(None))
            self.set_totals(total)
            cache_manager.update_cache(total)
            return self.answer_totals(total)
        except Exception as e:
            logging.error(f"Error al obtener el resumen: {e}")
            raise

    def dif_summaries(self, cache_manager):
        try:
            if self.LAST_MONTH_TOTAL is None:
                self.LAST_MONTH_TOTAL = self.get_total(DateSetterLastMonth(None))
            return self.calculate_dif(self.LAST_MONTH_TOTAL, self.TOTAL)
        except Exception as e:
            logging.error(f"Error al obtener el resumen: {e}")
            raise

    def answer_totals(self, new_total):
        return f"El total actual es: {new_total}. Se obtuvieron {new_total - self.LAST_TOTAL} pesos más que la anterior vez."

    def calculate_dif(self, last_month_total, current_total):
        dif = current_total - last_month_total
        porcent = (dif / last_month_total) * 100
        more_or_lower = 'menos' if porcent < 0 else 'mas'
        return f"El mes pasado a esta altura se hicieron: {last_month_total} de pesos. Por lo tanto, se obtuvo un {porcent}% {more_or_lower} que el mes anterior. Habiendo una diferencia de {dif} de pesos entre ambos."

    def set_totals(self, new_total):
        if self.LAST_TOTAL == 0 and self.TOTAL == 0:
            self.TOTAL = new_total
        if self.TOTAL != 0:
            self.LAST_TOTAL = self.TOTAL
            self.TOTAL = new_total

    def get_total(self, date_setter):
        self.web_driver_manager.set_date_setter(date_setter)
        self.web_driver_manager.start(self.BASE_URL, self.DB_USER, self.DB_PASSWORD)
        return self.get_excel_total()

    def get_excel_total(self):
        path = self.web_driver_manager.get_downloaded_file_path()
        excel_reader = ExcelReader(path)
        return float(excel_reader.get_total())
