# selenium imports
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service   
from selenium.webdriver.common.by import By 
from selenium import webdriver
# automatition methods
from application.models.automation.date_setter.DateSetterCurrentMonth import DateSetterCurrentMonth
from application.models.automation.report_module import navigate_to_report
from application.models.automation.login_module import login
from application.models.automation.file_downloader_module import download_file 
#registrar errores
import logging 
# to get .env info
from decouple import config  
import time
# path where excel file gonna be download 
from abs_path import dir

class WebDriverManager:
    _instance = None

    BASE_URL = "https://game.systemmaster.com.ar/frmLogin.aspx"
    DB_USER = config("DB_USER")
    DB_PASSWORD = config("DB_PASSWORD")
    EXPECTED_FILENAME_PATTERN = "rptCobranzas*.xls"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WebDriverManager, cls).__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):  # Para evitar re-inicialización
            self.driver = None
            self.configure_driver()
            self.date_setter = DateSetterCurrentMonth(self.driver)
            self.initialized = True

    def configure_driver(self):
        try:
            service = Service(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()

            # First environment configs and headless mode 
            options.add_argument("--headless=new") 
            options.add_argument("--no-sandbox")  
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")  
            options.add_argument("--disable-software-rasterizer")
            
            # Configuraciones de rendimiento y comportamiento
            options.add_argument("--disable-extensions") 
            options.add_argument("--window-size=1280,720")  
            options.add_argument("--disable-logging") 
            options.add_argument("--disable-animations")  

            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("--use-gl=disabled")
            options.add_argument("--disable-webgl")
            options.add_argument("--disable-3d-apis")

            options.add_experimental_option("prefs", {
                "profile.managed_default_content_settings.images": 2, 
                "profile.default_content_setting_values.notifications": 2,  
                "download.default_directory": dir, 
                "safebrowsing.enabled": True  
            })
            self.driver = webdriver.Chrome(service=service, options=options)
            self.start_time = time.time()
        except Exception as e:
            logging.error(f"Error al configurar el WebDriver: {e}")
            raise e

    def should_restart_driver(self):
        return time.time() - self.start_time > 30 #86400

    def quit_driver(self):
        if self.driver and self.should_restart_driver():
            self.driver.quit()
            self.configure_driver()
    
    def go_to_report_page(self):
        try:
            self.driver.get(self.BASE_URL)
            login(self.DB_USER, self.DB_PASSWORD, self.driver)
            navigate_to_report(self.driver)
            # click on 'Resumen' button
            self.driver.find_element(By.ID, "ctl15_chkResumen").click()
        except Exception as e:
            logging.error(f"Error al navegar a la página de reportes: {e}")
            raise

    def set_dates_and_download(self):
        try:
            self.set_dates()
            return self.download_file()
        except Exception as e:
            logging.error(f"Error al settear fechas y descargar archivo: {e}")
            raise

    def set_dates(self):
       self.date_setter.set()

    def download_file(self):
        return download_file(self.driver, dir, self.EXPECTED_FILENAME_PATTERN, timeout=30)

    def get_driver(self):
        if self.driver is None:
            raise Exception("El driver no está configurado.")
        return self.driver

    def set_date_setter(self, date_setter):
        date_setter.set_driver(self.driver)
        self.date_setter = date_setter
