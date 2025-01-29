from .DateSetterLastMonth import DateSetterLastMonth
from datetime import datetime
import pytz 

class DateSetterLastMonthToday(DateSetterLastMonth):

    def get_fecha_cobro_hasta(self, today):
        return today.strftime("%d/%m/%Y") 
    
    def update_info(self, summary, amount):
        print(f"Se settio el set_last_months_total_today a {amount}")
        summary.set_last_months_total_today(amount)

    def is_necessary_again(self, summary):
        return (datetime.now(pytz.timezone("America/Argentina/Buenos_Aires")).date() != summary.get_date_of_lmtt().date())