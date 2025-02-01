from selenium.webdriver.common.by import By 
import logging 

def fill_input(driver, id, keys):
    input = driver.find_element(By.ID, id)
    input.send_keys(keys)

def login(user, password, driver):
    try: 
        if not user or not password:
            raise ValueError("No username or password provided")
        
        fill_input(driver,"txtUsuarioId", user)
        logging.info("User written")
        print("User written")
        
        fill_input(driver,"txtClave", password)
        logging.info("Password written")
        print("Password written")
        
        login_button = driver.find_element(By.ID,"btnLogin")
        login_button.click()
        
        logging.info("Clicked Login Button")
        print("Clicked Login Button")
    
    except Exception as e: 
        raise Exception(f"Error while logging in: {e}")
    