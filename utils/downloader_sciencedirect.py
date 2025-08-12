from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

class ScienceDirectDownloader:
    def __init__(self, download_dir, headless=False):
        options = Options()
        prefs = {"download.default_directory": download_dir}
        options.add_experimental_option("prefs", prefs)
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

    def download(self, query):
        print("[INFO] Abriendo ScienceDirect...")
        self.driver.get("https://www.sciencedirect.com/")

        # Esperar a que aparezca el cuadro de búsqueda
        search_box = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='search-input']"))
        )
        search_box.clear()
        search_box.send_keys(query)
        search_box.submit()

        # Esperar resultados
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "search-result-content"))
        )

        time.sleep(2)  # Pausa breve para asegurar carga
        print("[INFO] Resultados cargados en ScienceDirect. (Aquí iría la lógica de descarga)")

    def close(self):
        self.driver.quit()
