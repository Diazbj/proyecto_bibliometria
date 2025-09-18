import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import glob
import shutil


class ACMDescarga:
    def __init__(self):
        # Carpeta base de descargas en tu proyecto
        base_dir = r"C:\Users\DiazJ\PycharmProjects\ProyectoAnalisisAlgoritmo\proyecto_bibliometria\descargas"

        # Subcarpeta descargaACM dentro de esa ruta
        self.download_dir = os.path.join(base_dir, "descargaACM")
        os.makedirs(self.download_dir, exist_ok=True)

        # Configuración Chrome
        options = uc.ChromeOptions()
        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)

        # Abrir Chrome
        self.driver = uc.Chrome(headless=False, options=options)
        self.wait = WebDriverWait(self.driver, 20)
        self.wait_long = WebDriverWait(self.driver, 40)
        self.driver.maximize_window()

    def esperar_overlay(self):
        """Espera a que desaparezca el overlay de carga."""
        try:
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "onload-background")))
        except:
            pass

    def aceptar_cookies(self):
        """Acepta cookies si aparecen."""
        try:
            cookie_btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
            )
            cookie_btn.click()
            print("Cookies aceptadas.")
        except:
            pass

    def esperar_descarga(self, timeout=120):
        """Espera hasta que no haya archivos .crdownload en la carpeta."""
        start_time = time.time()
        while True:
            cr_files = glob.glob(os.path.join(self.download_dir, "*.crdownload"))
            if not cr_files:  # no hay descargas en progreso
                break
            if time.time() - start_time > timeout:
                print("⚠️ Tiempo de espera agotado para la descarga.")
                break
            time.sleep(1)  # espera 1 segundo y revisa de nuevo

    def renombrar_descarga(self, page_num):
        """Renombra el último archivo descargado a extensión .bib"""
        files = sorted(
            glob.glob(os.path.join(self.download_dir, "*")),
            key=os.path.getmtime,
            reverse=True
        )
        if files:
            last_file = files[0]
            new_name = os.path.join(self.download_dir, f"pagina_{page_num:02d}.bib")
            try:
                shutil.move(last_file, new_name)
                print(f" Archivo renombrado a {new_name}")
            except Exception as e:
                print(f"Error al renombrar archivo: {e}")

    def abrir_base_datos(self, query):
        self.driver.get("https://library.uniquindio.edu.co/databases")

        self.esperar_overlay()

        # Ir a "BASES DATOS x FACULTAD"
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "BASES DATOS x FACULTAD"))).click()
        self.esperar_overlay()

        # Click en facultad de ingeniería
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@data-content-listing-item='fac-ingenier-a']")
        )).click()
        self.esperar_overlay()

        # Click en ACM
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[@href='https://dl.acm.org/']")
        )).click()

        # Cambiar a nueva pestaña
        self.driver.switch_to.window(self.driver.window_handles[-1])

        # Buscar
        search_box = self.wait.until(EC.visibility_of_element_located((By.NAME, "AllField")))
        search_box.clear()
        search_box.send_keys(query)
        self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.quick-search__button"))
        ).click()

        # Esperar resultados
        self.wait_long.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "li.search__item.issue-item-container")
        ))

        # Cambiar a 50 resultados por página
        try:
            link_50 = self.wait_long.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='per-page separator-end']//a[contains(@href,'pageSize=50')]")
            ))
            self.driver.execute_script("arguments[0].click();", link_50)
            self.wait_long.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "li.search__item.issue-item-container")
            ))
        except:
            print("No se pudo cambiar a 50 resultados por página.")

        # Descargar todas las páginas
        page_num = 1
        while True:
            self.aceptar_cookies()

            # Seleccionar todos
            select_all = self.wait_long.until(EC.element_to_be_clickable((By.NAME, "markall")))
            self.driver.execute_script("arguments[0].click();", select_all)
            self.wait_long.until(lambda d: select_all.is_selected())

            # Exportar
            export_btn = self.wait_long.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.export-citation")))
            self.driver.execute_script("arguments[0].click();", export_btn)
            time.sleep(2)

            # Descargar
            download_btn = self.wait_long.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.download__btn")))
            self.driver.execute_script("arguments[0].click();", download_btn)

            # Esperar que el archivo realmente se descargue
            print(f"⏳ Esperando descarga de página {page_num} ...")
            self.esperar_descarga(timeout=120)
            self.renombrar_descarga(page_num)  # <-- Renombrar a .bib
            print(f"✅ Página {page_num} descargada.")

            # Cerrar modal
            try:
                close_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.close[data-dismiss='modal']"))
                )
                close_btn.click()
            except:
                pass

            # Pausa antes de ir a la siguiente página
            time.sleep(3)

            # Siguiente página
            try:
                next_page = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.pagination__btn--next"))
                )
                self.driver.execute_script("arguments[0].click();", next_page)
                self.wait_long.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "li.search__item.issue-item-container")
                ))
                page_num += 1
                print("➡️ Página siguiente cargada.")
            except:
                print("🏁 No hay más páginas.")
                break

    def cerrar(self):
        self.driver.quit()


if __name__ == "__main__":
    bot = ACMDescarga()
    bot.abrir_base_datos("\"generative artificial intelligence \"")
    bot.cerrar()
