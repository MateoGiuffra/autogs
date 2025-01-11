from .DateSetterLastMonth import DateSetterLastMonth

class DateSetterLastMonthToday(DateSetterLastMonth):

    def get_fecha_cobro_hasta(self, today):
        return today.strftime("%d/%m/%Y") 
    
    def update_info(self, summary, amount):
        print(f"Se settio el set_last_months_total_today a {amount}")
        summary.set_last_months_total_today(amount)
        summary.set_message_last_months_total_today(summary.calculate_dif(amount, summary.get_total()))

    def get_field(self):
        return "last_months_total_today"
    
    def is_necesary_calculate(self):
        return True     
    
    def set_message(self, summary, json):
        summary.set_message_last_months_total_today(json)