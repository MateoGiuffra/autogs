from .DateSetter import DateSetter
import datetime
from dateutil import relativedelta 
import pytz 

class DateSetterCurrentMonth(DateSetter):

    def __init__(self, driver):
        super().__init__(driver)

    def get_today(self):
        tz_buenos_aires = pytz.timezone('America/Argentina/Buenos_Aires')
        now = datetime.datetime.now(tz_buenos_aires)
        return now.astimezone(tz_buenos_aires).date()
    
    def next_month_of_today(self, today):
        return today + relativedelta.relativedelta(months = 1)

    def get_fecha_cobro_hasta(self, today):
        return today.strftime("%d/%m/%Y")
    
    def update_info(self, summary, amount):
        summary.set_last_total(summary.get_total())
        summary.set_total(amount)
        summary.set_last_report_date(datetime.datetime.now())
    
    def get_field(self):
        return "total"
    
    def is_necesary_calculate(self):
        return True 