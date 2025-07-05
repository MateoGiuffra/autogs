from application.models.automation.date_setter.DateSetterCurrentMonth import DateSetterCurrentMonth
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service   
from selenium.webdriver.common.by import By 
from selenium import webdriver
# functions para la automatizacion
from application.models.automation.report_module import navigate_to_report
from application.models.automation.login_module import login
from application.models.automation.file_downloader_module import download_file 
#registrar errores
import logging 

import time
import os
import logging
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from application.models.automation.login_module import login
from application.models.automation.report_module import navigate_to_report
from application.models.automation.file_downloader_module import download_file
from application.models.automation.date_setter.DateSetterCurrentMonth import DateSetterCurrentMonth

class WebDriverManager:

    def __init__(self, output_path, expected_filename_pattern):
        self.expected_filename_pattern = expected_filename_pattern
        self.output_path = output_path
        os.makedirs(self.output_path, exist_ok=True)
        self.driver = None
        self.configure_driver()
        self.date_setter = DateSetterCurrentMonth(self.driver)



    def configure_driver(self):
        try:
            service = Service(ChromeDriverManager().install(), log_path="chromedriver.log")
            options = webdriver.ChromeOptions()

            options.add_argument("--headless=new")  
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1280,720")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-logging")

            prefs = {
                "profile.default_content_settings.popups": 0,
                "download.default_directory": self.output_path,
                "directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            options.add_experimental_option("prefs", prefs)

            self.driver = webdriver.Chrome(service=service, options=options)
            self.start_time = time.time()

        except Exception as e:
            logging.error(f"Error al configurar WebDriver: {e}")
            raise e

    def start(self, url, user, password):
        try:
            self.driver.get(url)
            login(user, password, self.driver)
            navigate_to_report(self.driver)
            self.set_dates()
            return self.download_file()
        except Exception as e:
            logging.error(f"Error al iniciar navegador: {e}")
            print(f"Hubo un error al iniciar: {e}")
            raise
        finally:
            self.driver.quit()

    def set_dates(self):
        self.date_setter.set()

    def download_file(self):
        self.driver.find_element(By.ID, "ctl15_chkResumen").click()
        return download_file(self.driver, self.output_path, self.expected_filename_pattern, timeout=30)

    def get_driver(self):
        if self.driver is None:
            raise Exception("El driver no está configurado.")
        return self.driver

    def set_date_setter(self, date_setter):
        date_setter.set_driver(self.driver)
        self.date_setter = date_setter
