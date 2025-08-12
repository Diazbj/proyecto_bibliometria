import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class ACMDownloader:
    def __init__(self, download_dir, headless=True):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        prefs = {"download.default_directory": download_dir}
        options.add_experimental_option("prefs", prefs)

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 20)

    def download(self, query):
        try:
            print("[INFO] Abriendo ACM Digital Library...")
            self.driver.get("https://dl.acm.org/")

            wrapper = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.autoComplete_wrapper"))
            )
            search_box = wrapper.find_element(By.CSS_SELECTOR, "input[name='AllField']")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", search_box)
            time.sleep(0.5)
            search_box.click()
            search_box.clear()
            search_box.send_keys(query)
            search_box.submit()

            self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.search__item"))
            )

            print(f"[INFO] Resultados de ACM para '{query}' descargados (simulación).")
        except Exception as e:
            print(f"[ERROR] No se pudo buscar en ACM: {e}")

    def close(self):
        self.driver.quit()
