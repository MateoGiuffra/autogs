from selenium.webdriver.common.by import By 

def login(user, password, driver):
    if user != None and password != None:
        user_input = driver.find_element(By.ID, "txtUsuarioId")
        user_input.send_keys(user)
        print("Usuario escrito")
        
        password_input = driver.find_element(By.ID, "txtClave")
        password_input.send_keys(password)
        print("Contraseña escrita")

        login_button = driver.find_element(By.ID,"btnLogin")
        login_button.click()
        print("Botón de Login clickeado")
    else: 
        raise Exception("No se puso usuario o contraseña")
