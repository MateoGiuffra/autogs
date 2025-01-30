from selenium.webdriver.common.by import By 
from abc import ABC, abstractmethod

class DateSetter(ABC):
    def __init__(self, driver):
        self.driver = driver

    def set(self):   
        today = self.get_today()

        fecha_cobro_desde = self.set_first_day_of(today)
        self.set_date_str(fecha_cobro_desde, "ctl15$FechaDesde$txtFecha")

        next_month = self.next_month_of_today(today)
        fecha_vto_desde =  self.set_first_day_of(next_month)
        self.set_date_str(fecha_vto_desde, "ctl15$FechaVtoDesde$txtFecha")

        fecha_cobro_hasta = self.get_fecha_cobro_hasta(today)
        self.set_date_str(fecha_cobro_hasta, "ctl15$FechaHasta$txtFecha")
        
        print("Fechas setteadas con exito")

    def set_date_str(self, date_str, name):
        date = self.driver.find_element(By.NAME, name)
        date.clear()
        date.send_keys(date_str)

    def set_first_day_of(self, today):
        return today.replace(day=1).strftime("%d/%m/%Y")

    @abstractmethod
    def get_fecha_cobro_hasta(self, today):
        pass 

    @abstractmethod
    def next_month_of_today(self, today):
        pass
    
    @abstractmethod
    def get_today(self):
        pass 

    @abstractmethod
    def update_info(self, summary, amount):
        pass

    def set_driver(self, driver):
        self.driver = driver 
    
    @abstractmethod    
    def is_necessary_again(month_and_year, summary_json, service):
        pass

