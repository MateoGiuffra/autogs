from decouple import config  
from application.automation.WebDriverManager import WebDriverManager
from application.pandas.ExcelReader import ExcelReader
from AbsPath import AbsPath


class SummaryService:
        
    @staticmethod
    def get_summary(url, user, password):
        output_path = AbsPath.obtener_abspath()
        expected_filename_pattern = 'rptCobranzas*.xls'
        web_driver_manager = WebDriverManager(output_path, expected_filename_pattern )
        web_driver_manager.start(url, user, password)

        path = web_driver_manager.get_downloaded_file_path()
        excel_reader = ExcelReader(path)

        return excel_reader.get_total() 


   

