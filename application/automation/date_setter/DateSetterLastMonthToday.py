from .DateSetterLastMonth import DateSetterLastMonth

class DateSetterLastMonthToday(DateSetterLastMonth):

    def get_fecha_cobro_hasta(self, today):
        return today.strftime("%d/%m/%Y") 
    
    def set_summary_total(self, summary, amount):
        summary.set_last_months_total_today(amount)

    def get_field(self):
        return "last_months_total_today"