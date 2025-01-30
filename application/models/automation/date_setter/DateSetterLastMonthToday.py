from .DateSetterLastMonth import DateSetterLastMonth
from datetime import datetime
import pytz
from application.persistence.SummaryDAO import SummaryDAO 

class DateSetterLastMonthToday(DateSetterLastMonth):

    def get_fecha_cobro_hasta(self, today):
        return today.strftime("%d/%m/%Y") 
    
    def update_info(self, summary, amount):
        print(f"Se settio el set_last_months_total_today a {amount}")
        summary.set_last_months_total_today(amount)

    def is_necessary_again(self, month_and_year, summary_json, service):
        
        date_of_lmtt = summary_json["date_of_lmtt"]
        
        real_today = datetime.now(pytz.timezone("America/Argentina/Buenos_Aires"))
        if (not summary_json or "date_of_lmtt" not in summary_json or real_today.date() != date_of_lmtt.date()):
            service.update_field_of(month_and_year,"date_of_lmtt", real_today)
            return True 

        return False