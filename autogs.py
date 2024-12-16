from selenium import webdriver
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.service import Service   
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 

def main():
# configuro los argumentos para mi driver
   
    driver
    options 
    service  

try: 
    
    service = Service(ChromeDriverManager().install()) #instalo el chrome por si no lo tiene la maquina que corre el script
    options = webdriver.ChromeOptions()  #es para personalizar chrome en este caso
    # option.add_argument("--headless") esta me sirve para que se ejecute minimizado
    options.add_argument("--window-size=1920,1080") # esta opcion es para asignarle un tamaño a la pagina
    driver = Chrome(service=service, options= options)

    driver = Chrome(service=service, options= options)
    driver.get("https://game.systemmaster.com.ar/frmLogin.aspx") 
    
    user_input = driver.find_element(By.XPATH, "/html/body/div[1]/div/form/fieldset/div/div/label[1]/span/input")
    user_input.send_keys("giuffraa")
    password_input = driver.find_element(By.XPATH, "/html/body/div[1]/div/form/fieldset/div/div/label[2]/span/input")
    password_input.send_keys("12345")
    

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

    cobranzas.click()
    time.sleep(10)
    calendar = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[3]/div[2]/table/tbody/tr[6]/td[2]/table/tbody/tr[2]/td[2]/input")
    calendar.click()
    #abro el calendario
    
except Exception as e: 
    print(f"Error: {e}")
    # time.sleep(2)
    
finally:    
    driver.quit()

if __name__ == "__main__":
    main()
