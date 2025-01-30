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

class WebDriverManager:

    def __init__(self, output_path, expected_filename_pattern ):
        self.expected_filename_pattern = expected_filename_pattern
        self.output_path = output_path
        self.driver = None
        self.configure_driver()
        self.file_downloaded_path = None
        self.date_setter =  DateSetterCurrentMonth(self.driver)
    
    def configure_driver(self):
        self.initialize_logging()
        try:
            service = Service(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()

            # Primero las configuraciones de entorno y modo sin cabeza
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

            # Configuración de preferencias
            options.add_experimental_option("prefs", {
                "profile.managed_default_content_settings.images": 2, 
                "profile.default_content_setting_values.notifications": 2,  
                "download.default_directory": self.output_path, 
                "safebrowsing.enabled": True  
            })

            # Inicializa el WebDriver con las opciones configuradas
            self.driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            logging.error(f"Error al configurar el WebDriver: {e}")
            raise e

    
    def initialize_logging(self):
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='webdriver_errors.log',
            filemode='a'
        )

    def start(self, url, user, password):
        try: 
            self.driver.delete_all_cookies()
            self.driver.get(url)
            
            login(user, password, self.driver)
            navigate_to_report(self.driver)       
            self.set_dates()
            self.download_file()
        except Exception as e:
            print(f"Hubo un error al iniciar: {e}")
            print(str(e))
            raise 
        finally:
            self.quit_driver()

    def set_dates(self):
       self.date_setter.set()

    def download_file(self):
        #click en resumen
        self.driver.find_element(By.ID, "ctl15_chkResumen").click()
        self.file_downloaded_path = download_file(self.driver, self.output_path, self.expected_filename_pattern, timeout=30)

    def get_downloaded_file_path(self):
        return self.file_downloaded_path

    def get_driver(self):
        if self.driver is None:
            raise Exception("El driver no está configurado.")
        return self.driver

    def quit_driver(self):
        if self.driver:
            self.driver.quit()

    def set_date_setter(self, date_setter):
        date_setter.set_driver(self.driver)
        self.date_setter = date_setter