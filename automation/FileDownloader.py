from selenium.webdriver.common.by import By
import glob
import time 
import os 

class FileDownloader:

    def __init__(self,driver,output_path,expected_filename_pattern):
        self.driver = driver
        self.output_path = output_path
        self.expected_filename_pattern = expected_filename_pattern

    def download(self):
        download_button = self.driver.find_element(By.NAME, "ctl15$btnConsultar")
        download_button.click()

        wait_time = 20  # Tiempo máximo de espera
        start_time = time.time()
        
        downloaded_file_path = None 

        while time.time() - start_time < wait_time:
            # Buscar archivos que coincidan con el patrón
            file_pattern = os.path.join(self.output_path, self.expected_filename_pattern)
            matching_files = glob.glob(file_pattern)
            
            if matching_files:
                # Si encontramos archivos que coinciden, asignamos el primero encontrado
                downloaded_file_path = matching_files[0]
                print(f"El archivo se descargó correctamente: {downloaded_file_path}")
                return downloaded_file_path  # Retorna la ruta del archivo descargado

            time.sleep(1)  # Esperar 1 segundo antes de verificar nuevamente
        
        # Si no se encuentra ningún archivo dentro del tiempo esperado, retornar None
        return None

        # # Esperar hasta que el archivo esté presente o se alcance el tiempo máximo
        # while time.time() - start_time < wait_time:
        #     # Buscar archivos que coincidan con el patrón
        #     file_pattern = os.path.join(self.output_path, self.expected_filename_pattern)
        #     matching_files = glob.glob(file_pattern)
            
        #     if matching_files:
        #         # Si hay coincidencias, asignamos el primero encontrado
        #         downloaded_file_path = matching_files[0]
        #         break                

        #     time.sleep(1)  
        
        # return downloaded_file_path