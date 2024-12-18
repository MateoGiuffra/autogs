import datetime
from selenium.webdriver.common.by import By 
from dateutil import relativedelta 

import datetime
from dateutil import relativedelta
from selenium.webdriver.common.by import By

class DateSetter:
    def __init__(self, driver):
        self.driver = driver

    def set(self):        
        today = datetime.date.today()
        
        # El primer día del mes
        firstDayOfThisMonth = self.set_first_day_of(today)
        self.set_date_str(firstDayOfThisMonth, "ctl15$FechaDesde$txtFecha")
        
        # El primer día del próximo mes
        nextmonth = today + relativedelta.relativedelta(months=1)
        firstDayOfNextMonth = self.set_first_day_of(nextmonth)
        
        self.set_date_str(firstDayOfNextMonth, "ctl15$FechaVtoDesde$txtFecha")

    def set_date_str(self, date_str, name):
        date = self.driver.find_element(By.NAME, name)
        date.clear()
        date.send_keys(date_str)

    def set_first_day_of(self, today):
        return today.replace(day=1).strftime("%d/%m/%Y")


  
