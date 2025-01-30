from .DateSetter import DateSetter
import datetime
from dateutil import relativedelta 
import pytz
from decouple import config 
TIMEZONE = config("TIMEZONE", default = 'America/Argentina/Buenos_Aires')
class DateSetterLastMonth(DateSetter):

    def __init__(self, driver):
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
    
    def is_necessary_again(self, month_and_year, summary_json, service):
        if not summary_json or "date_of_lmt" not in summary_json:
            return True 
        
        date_of_lmt = summary_json["date_of_lmt"]
        

        real_today = datetime.datetime.now(pytz.timezone("America/Argentina/Buenos_Aires"))
        # and real_today.year() != date_of_lmt.year()
        if date_of_lmt is None or not summary_json or "date_of_lmtt" not in summary_json or (real_today.month != date_of_lmt.month and real_today.year != date_of_lmt.year):
            service.update_field_of(month_and_year, "date_of_lmt", real_today)
            return True 
        
        return False

    

    