from .DateSetter import DateSetter
import datetime
from dateutil import relativedelta 

class DateSetterLastMonth(DateSetter):

    def __init__(self, driver):
        super().__init__(driver)

    def get_today(self):
        today = datetime.date.today()
        return today + relativedelta.relativedelta(months = -1)
    
    def next_month_of_today(self, today):
        return datetime.date.today()
    


  
