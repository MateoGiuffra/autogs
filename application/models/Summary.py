# automatition methods
from application.models.automation.WebDriverManager import WebDriverManager
from application.models.pandas.excel_reader import reader_get_total

# time libraries  
from datetime import datetime
import pytz 
import time 
# environment library
from decouple import config

TIMEZONE = config("TIMEZONE", default="America/Argentina/Buenos_Aires")
class Summary:
    def __init__(self, month_and_year):
        self.month_and_year = month_and_year
        self.total = 0
        self.last_total = 0
        self.last_months_total = 0
        self.last_months_total_today = 0
        self.last_report_date = time.strftime("%d-%m-%Y %H:%M:%S")
        self.date_of_lmtt = None
        self.date_of_lmt = None

    def get_total_number(self, date_setter):
        try: 
            webdrivermanager = WebDriverManager()
            path = webdrivermanager.set_dates_and_download()
            self.total = float(reader_get_total(path))
            date_setter.update_info(self, self.total)
            return self.total
        except Exception as e:
            raise Exception(f"Something was Wrong to get total number: {e}")
    
    # devuelve un JSON con la informacion del objeto
    def to_summary_dict(self):
        return {
            "total": self.total,  
            "last_total": self.last_total,  
            "last_months_total": self.last_months_total,   
            "last_months_total_today": self.last_months_total_today, 
            "last_report_date" : self.last_report_date,
            "date_of_lmtt": self.date_of_lmtt,
            "date_of_lmt": self.date_of_lmt
        }
    
    @classmethod
    def from_dict(cls, month_and_year, data):
        instance = cls(month_and_year)
        instance.total = float(data.get("total", 0))
        instance.last_total = float(data.get("last_total", 0))
        instance.last_months_total = float(data.get("last_months_total", 0))
        instance.last_months_total_today = float(data.get("last_months_total_today", 0))
        instance.last_report_date = data.get("last_report_date", datetime.now(pytz.timezone("America/Argentina/Buenos_Aires")).strftime("%d-%m-%Y %H:%M:%S"))
        instance.date_of_lmtt = data.get("date_of_lmtt", None)
        instance.date_of_lmt  = data.get("date_of_lmt", None)
        return instance
    
   # getters  
    def get_date_of_lmt(self):
        return self.date_of_lmt
    
    def get_date_of_lmtt(self):
        return self.date_of_lmtt
    
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
        
    def set_date_of_lmtt(self, lmtt_date):
        self.date_of_lmtt = lmtt_date 
        
    def set_date_of_lmt(self, lmt_date):
        self.date_of_lmt = lmt_date 
    
    def set_last_total(self, last_total):
        self.last_total = last_total

    def set_last_months_total(self, last_months_total):
        self.last_months_total = last_months_total   
        
    def set_last_months_total_today(self, last_months_total_today):
        self.last_months_total_today = last_months_total_today         
        
    

        

        