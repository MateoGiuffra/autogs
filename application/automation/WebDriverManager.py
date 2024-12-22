from application.automation.Login import Login 
from application.automation.Report import Report 
from application.automation.date_setter.DateSetterCurrentMonth import DateSetterCurrentMonth
from application.automation.FileDownloader import FileDownloader

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.service import Service   
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import os 
import logging 


class WebDriverManager:

    def __init__(self, output_path, expected_filename_pattern):
        self.output_path = output_path
        self.driver = None
        self.configure_driver()
        self.expected_filename_pattern = expected_filename_pattern
        self.file_downloaded_path = None
        self.login_page = Login(self.driver, None, None)
        self.report_page = Report(self.driver)
        self.date_setter = DateSetterCurrentMonth(self.driver)
        self.file_downloader = FileDownloader(self.driver, self.output_path, self.expected_filename_pattern)

    
    def configure_driver(self):
        self.initialize_logging()
        try:
            service = Service(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            # options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_experimental_option("prefs", {
                "download.default_directory": self.output_path,
                "safebrowsing.enabled": True
            })
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.set_page_load_timeout(30)
        except Exception as e: 
            logging.error(f"Error al configuar el WebDriver: {e}")
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
            try:
                self.driver.get(url)
            except Exception as a:
                print("Hubo error en el login: {a}")
                print(str(a))
                raise a
            self.login(user, password)
            self.navigate_to_report()        
            self.set_dates()
            #click on resume
            self.driver.find_element(By.ID, "ctl15_chkResumen").click()
            self.download_file()
            
            self.quit_driver()
        except Exception as e:
            print("Hubo un error al iniciar: {e}")
            raise

    def login(self, user, password):
        self.login_page.set_user(user)
        self.login_page.set_password(password)
        self.login_page.login()

    def navigate_to_report(self):
        self.report_page.navigate_to_report()

    def set_dates(self):
        self.date_setter.set()

    def download_file(self):
        self.file_downloaded_path = self.file_downloader.download()

    def get_downloaded_file_path(self):
        return self.file_downloaded_path

    def set_date_setter(self, date_setter):
        date_setter.set_driver(self.driver)
        self.date_setter = date_setter

    def get_driver(self):
        if self.driver is None:
            raise Exception("El driver no está configurado.")
        return self.driver

    def quit_driver(self):
        if self.driver:
            self.driver.quit()

    
