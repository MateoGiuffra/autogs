from decouple import config  # Si usas python-decouple

from selenium import webdriver
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.service import Service   
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import os 
from dateutil import relativedelta

import time 

def main():
    # creo las variables 
    # url
    url 
    # de user y password
    db_user 
    db_password 
    # configuro los argumentos para mi driver
    driver
    options 
    service  

try: 
    url = "https://game.systemmaster.com.ar/frmLogin.aspx"
    db_user = config("DB_USER")
    db_password = config("DB_PASSWORD")

    # Obtener la ruta absoluta del directorio actual (donde está el script)
    project_dir = os.path.dirname(os.path.abspath(__file__))

    # Combinar la ruta del proyecto con la carpeta "Output"
    output_dir = os.path.join(project_dir, "Output")

    # Crear la carpeta si no existe (opcional, para evitar errores)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    expected_filename = "archivo.xlsx"

    service = Service(ChromeDriverManager().install()) #instalo el chrome por si no lo tiene la maquina que corre el script
    options = webdriver.ChromeOptions()  #es para personalizar chrome en este caso
    # option.add_argument("--headless") esta me sirve para que se ejecute minimizado
    options.add_argument("--window-size=1920,1080") # esta opcion es para asignarle un tamaño a la pagina
    options.add_experimental_option("prefs", {
    "download.default_directory": output_dir,  # Carpeta personalizada
    "download.prompt_for_download": False,             # No mostrar diálogos
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
    })


    driver = Chrome(service=service, options= options)
    driver.get(url) 

   
    user_input = driver.find_element(By.XPATH, "/html/body/div[1]/div/form/fieldset/div/div/label[1]/span/input")
    user_input.send_keys(db_user)
    password_input = driver.find_element(By.XPATH, "/html/body/div[1]/div/form/fieldset/div/div/label[2]/span/input")
    password_input.send_keys(db_password)
    

    login_button = driver.find_element(By.XPATH,"/html/body/div[1]/div/form/fieldset/div/div/ul/li/span")
    login_button.click()
    
    reportes = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/form/div[3]/div[2]/table/tbody/tr/td/div[2]/table/tbody/tr/td[6]/nobr"))
    )
    # Usar ActionChains para mover el mouse sobre "Reportes" y abrir el menú desplegable
    actions = ActionChains(driver)
    actions.move_to_element(reportes).perform()

    # Esperar que el menú desplegable sea visible
    cobranzas_xpath = "//div[contains(text(),'Cobranzas')]"  # Ajusta el XPath según el texto o estructura
    cobranzas = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, cobranzas_xpath))
    )
    #voy a la pagina de cobranzas 
    cobranzas.click()

    #abro el calendario
    # calendar = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[3]/div[2]/table/tbody/tr[6]/td[2]/table/tbody/tr[2]/td[2]/input")
    # calendar.click()

    #el primer dia del mes
    firstDayOfThisMonth = datetime.date.today().replace(day=1)
    formattedFDOTM = firstDayOfThisMonth.strftime("%d/%m/%Y")

    fechaCobroDesde = driver.find_element(By.NAME, "ctl15$FechaDesde$txtFecha")
    fechaCobroDesde.clear()
    fechaCobroDesde.send_keys(formattedFDOTM)
    
    #el primer dia del proximo mes
    nextmonth = datetime.date.today() + relativedelta.relativedelta(months=1)
    firstDayOfNextMonth = nextmonth.replace(day=1)
    formattedDateFDONM = firstDayOfNextMonth.strftime("%d/%m/%Y")

    fechaVtoDeste = driver.find_element(By.NAME, "ctl15$FechaVtoDesde$txtFecha")
    fechaVtoDeste.clear()
    fechaVtoDeste.send_keys(formattedDateFDONM)

    #click en resumen
    resume_button = driver.find_element(By.ID, "ctl15_chkResumen")
    resume_button.click()
    
    # Esperar hasta que el archivo exista en la carpeta de descargas    
    download_button = driver.find_element(By.NAME,"ctl15$btnConsultar")
    download_button.click()

    wait_time = 20  # Tiempo máximo de espera
    start_time = time.time()

    while not os.path.exists(os.path.join(output_dir, expected_filename)):
        time.sleep(1)
        if time.time() - start_time > wait_time:
            raise TimeoutError("El archivo no se descargó dentro del tiempo esperado.")
    
except Exception as e: 
    print(f"Error: {e}")
    # time.sleep(2)
     
finally:    
    driver.quit()


if __name__ == "__main__":
    main()
