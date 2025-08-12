import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ACMDescarga:
    def __init__(self):
        # Inicializar Chrome con undetected_chromedriver
        self.driver = uc.Chrome(headless=False)
        self.driver.maximize_window()

    def abrir_base_datos(self):
        url = "https://library.uniquindio.edu.co/databases"
        self.driver.get(url)

        wait = WebDriverWait(self.driver, 15)

        # Esperar a que desaparezca el overlay inicial
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "onload-background")))

        # Clic en "BASES DATOS x FACULTAD"
        enlace = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "BASES DATOS x FACULTAD")))
        enlace.click()

        # Esperar overlay de nuevo por si hay animación
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "onload-background")))

        # Clic en "Fac. Ingeniería"
        elemento = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-content-listing-item='fac-ingenier-a']")))
        elemento.click()

        # Clic en enlace ACM Digital Library
        acm_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='https://dl.acm.org/']")))
        acm_link.click()

        # Cambiar a la nueva pestaña abierta
        self.driver.switch_to.window(self.driver.window_handles[-1])

        # Esperar a que aparezca el campo de búsqueda
        search_box = wait.until(EC.visibility_of_element_located((By.NAME, "AllField")))
        search_box.clear()
        search_box.send_keys("generative artificial intelligence")

        # Esperar a que el botón de búsqueda sea clickeable y hacer clic
        search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.quick-search__button")))
        search_button.click()

    def cerrar(self):
        self.driver.quit()


if __name__ == "__main__":
    bot = ACMDescarga()
    bot.abrir_base_datos()
    input("Presiona Enter para cerrar el navegador...")
    bot.cerrar()
