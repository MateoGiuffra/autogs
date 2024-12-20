from selenium.webdriver.common.by import By 

class Login:

    def __init__(self, driver, user, password):
        self.driver = driver
        self.user = user
        self.password = password

    def login(self):
        if self.user and self.password:
            user_input = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/form/fieldset/div/div/label[1]/span/input")
            user_input.send_keys(self.user)
            
            password_input = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/form/fieldset/div/div/label[2]/span/input")
            password_input.send_keys(self.password)
            
            login_button = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/form/fieldset/div/div/ul/li/span")
            login_button.click()
        else: 
            raise Exception("NO HAY USER NI CONTRASEÑA PAPA COMO HAGO??")