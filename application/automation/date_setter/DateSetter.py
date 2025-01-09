from selenium.webdriver.common.by import By 
from abc import ABC, abstractmethod

class DateSetter(ABC):
    def __init__(self, driver):
        self.driver = driver

    def set(self):   
        today = self.get_today()
        print(f"Hoy es {today}")
        fecha_cobro_desde = self.set_first_day_of(today)
        print(f"El primer dia del mes requerido para fecha desde es: {fecha_cobro_desde}")
        self.set_date_str(fecha_cobro_desde, "ctl15$FechaDesde$txtFecha")

        next_month = self.next_month_of_today(today)
        fecha_vto_desde =  self.set_first_day_of(next_month)
        print(f"El primer dia del mes requerido para la fecha de vencimiento es: {fecha_vto_desde}")
        self.set_date_str(fecha_vto_desde, "ctl15$FechaVtoDesde$txtFecha")

        fecha_cobro_hasta = self.get_fecha_cobro_hasta(today)
        print(f"La fecha requerida para la fecha cobro hasta es: {fecha_cobro_hasta}")
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

    @abstractmethod 
    def get_field(self):
        pass    

    @abstractmethod
    def is_necesary_calculate(self):
        pass   
    
    def set_message(self, summary, json):
        pass

    def set_driver(self, driver):
        self.driver = driver 

