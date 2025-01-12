import os
import time
from selenium.webdriver.common.by import By

def clear_output_directory(output_path):
    # Directamente obtener el único archivo y eliminarlo
    file = next(os.scandir(output_path), None)
    if file and file.is_file():
        os.remove(file.path)
        print(f"Archivo eliminado: {file.name}")
    else:
        print("No se encontró ningún archivo para eliminar.")

def get_latest_file(output_path):
    # Obtener directamente el único archivo en el directorio
    file = next(os.scandir(output_path), None)
    if not file or not file.is_file() or not file.name.startswith("rptCobranzas") or not file.name.endswith(".xls"):
        raise FileNotFoundError("No se encontró ningún archivo con el patrón esperado.")
    
    print(f"Archivo encontrado: {file.name}")
    return file.path

def download_file(driver, output_path, expected_filename_pattern, timeout=30):
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


    
    

