import os
import time
from selenium.webdriver.common.by import By

def clear_output_directory(output_path):
    """Elimina todos los archivos en el directorio de salida."""
    for entry in os.scandir(output_path):
        if entry.is_file():
            os.remove(entry.path)
            print(f"Archivo eliminado: {entry.name}")
    
def get_latest_file(output_path):
    """Obtiene el archivo más reciente basado en la fecha de modificación."""
    files = [
        entry for entry in os.scandir(output_path)
        if entry.name.startswith("rptCobranzas") and entry.name.endswith(".xls")
    ]
    if not files:
        raise FileNotFoundError("No se encontró ningún archivo con el patrón esperado.")
    
    latest_file = max(files, key=lambda f: f.stat().st_mtime)
    print(f"Archivo más reciente encontrado: {latest_file.name}")
    return latest_file.path

def download_file(driver, output_path, expected_filename_pattern, timeout=30):
    """Función principal para descargar el archivo."""
    start_time = time.time()

    # Vaciar la carpeta de salida
    clear_output_directory(output_path)

    # Hacer clic en el botón de descarga
    download_button = driver.find_element(By.NAME, "ctl15$btnConsultar")
    download_button.click()
    print("Botón de descarga clickeado.")

    # Esperar el archivo descargado
    while time.time() - start_time < timeout:
        try:
            return get_latest_file(output_path)
        except FileNotFoundError:
            time.sleep(1)  # Esperar antes de intentar nuevamente

    raise TimeoutError("No se encontró el archivo esperado dentro del tiempo especificado.")

    

    
    

