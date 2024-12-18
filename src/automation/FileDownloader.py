import os
import time
import glob
from selenium.webdriver.common.by import By

class FileDownloader:

    def __init__(self, driver, output_path, expected_filename_pattern):
        self.driver = driver
        self.output_path = output_path
        self.expected_filename_pattern = expected_filename_pattern

    def download(self):
        # Registrar los archivos existentes antes de descargar
        existing_files = set(glob.glob(os.path.join(self.output_path, self.expected_filename_pattern)))

        # Hacer clic en el botón de descarga
        download_button = self.driver.find_element(By.NAME, "ctl15$btnConsultar")
        download_button.click()

        wait_time = 7  # Tiempo máximo de espera
        start_time = time.time()
        downloaded_file_path = None

        # Esperar un nuevo archivo
        while time.time() - start_time < wait_time:
            # Buscar archivos que coincidan con el patrón
            search_pattern = os.path.join(self.output_path, self.expected_filename_pattern)
            matching_files = set(glob.glob(search_pattern))

            # Detectar un archivo nuevo que no estaba antes
            new_files = matching_files - existing_files

            if new_files:
                downloaded_file_path = new_files.pop()  # Obtener el primer archivo nuevo encontrado
                break  # Salir del bucle una vez encontrado el archivo nuevo

            time.sleep(1)  # Esperar antes de la siguiente verificación

        if downloaded_file_path:
            print(f"Archivo descargado correctamente: {downloaded_file_path}")
        else:
            print("No se encontró ningún archivo nuevo dentro del tiempo esperado.")
        
        return downloaded_file_path  # Retorna la ruta del archivo si se encontró

