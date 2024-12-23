from .DateSetter import DateSetter
import datetime
from dateutil import relativedelta 

class DateSetterCurrentMonth(DateSetter):

    def __init__(self, driver):
        super().__init__(driver)

    def get_today(self):
        return datetime.date.today()
    
    def next_month_of_today(self, today):
        return today + relativedelta.relativedelta(months = 1)

    def get_fecha_cobro_hasta(self, today):
        return today.strftime("%d/%m/%Y")