from .DateSetter import DateSetter
# import DateSetter
import datetime
from dateutil import relativedelta 
import sys

class DateSetterLastMonth(DateSetter):

    def __init__(self, driver):
        print(f"Base class: {DateSetter}")
        super().__init__(driver)

    def get_fecha_cobro_hasta(self, today):
        real_today = datetime.date.today()
        last_day = (real_today.replace(day=1) - relativedelta.relativedelta(days=1))
        return last_day.strftime("%d/%m/%Y") 

    def get_today(self):
        today = datetime.date.today()
        return today + relativedelta.relativedelta(months = -1)
    
    def next_month_of_today(self, today):
        return datetime.date.today()
    
