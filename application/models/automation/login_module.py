from selenium.webdriver.common.by import By 
import logging 

def fill_input(driver, id, keys):
    input = driver.find_element(By.ID, id)
    input.send_keys(keys)

def login(user, password, driver):
    try: 
        if not user or not password:
            raise ValueError("No se proporcionó usuario o contraseña")
        
        fill_input(driver,"txtUsuarioId", user)
        logging.info("Usuario escrito")
        
        fill_input(driver,"txtClave", password)
        logging.info("Contraseña escrita")
        
        login_button = driver.find_element(By.ID,"btnLogin")
        login_button.click()
        
        logging.info("Botón de Login clickeado")
    
    except Exception as e: 
        
        logging.info(f"Error al loggearse: {e}")
        raise Exception(f"Hubo un error al loggearse: {e}")
    