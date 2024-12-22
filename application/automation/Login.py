from selenium.webdriver.common.by import By 

class Login:

    def __init__(self, driver, user, password):
        self.driver = driver
        self.user = user
        self.password = password

    def login(self):
        if self.user and self.password:
            user_input = self.driver.find_element(By.ID, "txtUsuarioId")
            user_input.send_keys(self.user)
            print("Usuario escrito")
            
            password_input = self.driver.find_element(By.ID, "txtClave")
            password_input.send_keys(self.password)
            print("Contraseña escrita")

            login_button = self.driver.find_element(By.ID,"btnLogin")
            login_button.click()
            print("Botón de Login cleckeado")
        else: 
            raise Exception("No se puso usuario o contraseña")
        
    def set_user(self, user):
            self.user = user
            
    def set_password(self, password):
        self.password = password   
