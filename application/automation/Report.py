from selenium.webdriver.common.by import By 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Report():

    def __init__(self, driver):
        self.driver = driver


    def navigate_to_report(self):
        
        reportes = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/form/div[3]/div[2]/table/tbody/tr/td/div[2]/table/tbody/tr/td[6]/nobr"))
        )

        # Usar ActionChains para mover el mouse sobre "Reportes" y abrir el menú desplegable
        actions = ActionChains(self.driver)
        actions.move_to_element(reportes).perform()

        # Esperar que el menú desplegable sea visible
        cobranzas_xpath = "//div[contains(text(),'Cobranzas')]"  # Ajusta el XPath según el texto o estructura
        cobranzas = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, cobranzas_xpath))
        )
        
        #me dirijo a la pagina del reporte
        cobranzas.click()
