from automation.Login import Login 
from automation.Report import Report 
from automation.DateSetter import DateSetter
from automation.FileDownloader import FileDownloader

from selenium import webdriver
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.service import Service   
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait


class WebDriverManager:

    def __init__(self, output_path, expected_filename_pattern ):
        self.output_path = output_path
        self.driver = None
        self.configure_driver()
        self.expected_filename_pattern = expected_filename_pattern
        self.file_downloaded_path = None

    def configure_driver(self):
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_experimental_option("prefs", {
            "download.default_directory": self.output_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        self.driver = Chrome(service=service, options=options)

    def start(self, url, user, password):
        self.driver.get(url)
        
        self.login(user, password)
        self.navigate_to_report()        
        self.set_dates()
        #click on resume
        self.driver.find_element(By.ID, "ctl15_chkResumen").click()
        self.download_file()
        
        self.quit_driver()

       
    def login(self, user, password):
        login_page = Login(self.driver, user, password)
        login_page.login()


    def navigate_to_report(self):
        report_page = Report(self.driver)
        report_page.navigate_to_report()

    def set_dates(self):
        date_setter = DateSetter(self.driver)
        date_setter.set()

    def download_file(self):
        file_downloader = FileDownloader(self.driver, self.output_path, self.expected_filename_pattern)
        self.file_downloaded_path = file_downloader.download()

    def get_file_downloaded_path(self):
        return self.file_downloaded_path

    def get_driver(self):
        if self.driver is None:
            raise Exception("El driver no está configurado.")
        return self.driver

    def quit_driver(self):
        if self.driver:
            self.driver.quit()