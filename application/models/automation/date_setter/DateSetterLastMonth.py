from .DateSetter import DateSetter
import datetime
from dateutil import relativedelta 
import pytz
from decouple import config 
TIMEZONE = config("TIMEZONE", default = 'America/Argentina/Buenos_Aires')
class DateSetterLastMonth(DateSetter):

    def __init__(self, driver):
        print(f"Base class: {DateSetter}")
        super().__init__(driver)

    def get_fecha_cobro_hasta(self, today):
        real_today = datetime.date.today()
        last_day = (real_today.replace(day=1) - relativedelta.relativedelta(days=1))
        return last_day.strftime("%d/%m/%Y") 

    def get_today(self):
        tz_buenos_aires = pytz.timezone(TIMEZONE)
        now = datetime.datetime.now(tz_buenos_aires)
        today = now.astimezone(tz_buenos_aires).date()
        return today + relativedelta.relativedelta(months = -1)
    
    def next_month_of_today(self, today):
        tz_buenos_aires = pytz.timezone(TIMEZONE)
        now = datetime.datetime.now(tz_buenos_aires)
        return now.astimezone(tz_buenos_aires).date()
    

    def update_info(self, summary, amount):
        print(f"Se settio el set_last_months_total a {amount}")
        summary.set_last_months_total(amount)
    