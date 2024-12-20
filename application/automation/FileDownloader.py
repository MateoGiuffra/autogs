import os
import time
from selenium.webdriver.common.by import By

class FileDownloader:

    def __init__(self, driver, output_path, expected_filename_pattern):
        self.driver = driver
        self.output_path = output_path
        self.expected_filename_pattern = expected_filename_pattern

    def download(self):
        timeout = 30  # Tiempo máximo de espera
        start_time = time.time()

        # Vaciar la carpeta de salida
        self.clear_output_directory()

        # Hacer clic en el botón de descarga
        download_button = self.driver.find_element(By.NAME, "ctl15$btnConsultar")
        download_button.click()
        print("Botón de descarga clickeado.")

        # Esperar el archivo descargado
        while time.time() - start_time < timeout:
            try:
                return self.get_latest_file()
            except FileNotFoundError as e:
                time.sleep(1)  # Esperar antes de intentar nuevamente

        raise TimeoutError("No se encontró el archivo esperado dentro del tiempo especificado.")
    
    def clear_output_directory(self):
        """Elimina todos los archivos en el directorio de salida."""
        for entry in os.scandir(self.output_path):
            if entry.is_file():
                os.remove(entry.path)
                print(f"Archivo eliminado: {entry.name}")
                
    def get_latest_file(self):
        """Obtiene el archivo más reciente basado en la fecha de modificación."""
        files = [
            entry for entry in os.scandir(self.output_path)
            if entry.name.startswith("rptCobranzas") and entry.name.endswith(".xls")
        ]
        if not files:
            raise FileNotFoundError("No se encontró ningún archivo con el patrón esperado.")
        
        latest_file = max(files, key=lambda f: f.stat().st_mtime)
        print(f"Archivo más reciente encontrado: {latest_file.name}")
        return latest_file.path
                
    

    
    

