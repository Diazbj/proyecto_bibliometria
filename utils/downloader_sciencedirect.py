import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import glob
import shutil
import tempfile
import random


def human_wait(min_s=3, max_s=7):
    """Pausa aleatoria para simular comportamiento humano"""
    t = random.uniform(min_s, max_s)
    time.sleep(t)
    return t


def random_scroll(driver):
    """Simula scroll humano en posiciones aleatorias de la página"""
    try:
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        rand_position = random.randint(0, scroll_height)
        driver.execute_script(f"window.scrollTo(0, {rand_position});")
        human_wait(1, 4)
    except:
        pass


class ScienceDirectDescarga():
    def __init__(self):
        base_dir = r"C:\Users\DiazJ\PycharmProjects\ProyectoAnalisisAlgoritmo\proyecto_bibliometria\descargas"
        self.download_dir = os.path.join(base_dir, "descargaScienceDirect")
        os.makedirs(self.download_dir, exist_ok=True)

        tmp_profile = tempfile.mkdtemp()
        options = uc.ChromeOptions()
        options.add_argument(f"--user-data-dir={tmp_profile}")
        options.add_argument("--profile-directory=Default")
        options.add_argument("--disable-features=AccountConsistency,ChromeWhatsNewUI,SignInProfileCreation,SigninFrameSignInFlow,EnableEphemeralGuestProfilesOnDesktop")
        options.add_argument("--disable-sync")
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")

        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)

        self.driver = uc.Chrome(headless=False, options=options)
        self.wait = WebDriverWait(self.driver, 20)
        self.wait_long = WebDriverWait(self.driver, 40)
        self.driver.maximize_window()

    def esperar_overlay(self):
        try:
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "onload-background")))
        except:
            pass

    def aceptar_cookies(self):
        try:
            cookie_btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
            )
            cookie_btn.click()
            print(" Cookies aceptadas.")
            human_wait(2, 4)
        except:
            pass

    def esperar_descarga(self, timeout=180):
        start_time = time.time()
        while True:
            cr_files = glob.glob(os.path.join(self.download_dir, "*.crdownload"))
            if not cr_files:
                break
            if time.time() - start_time > timeout:
                print(" Tiempo de espera agotado para la descarga.")
                break
            time.sleep(1)

    def renombrar_descarga(self, page_num):
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
                print(f"Archivo renombrado a {new_name}")
            except Exception as e:
                print(f" Error al renombrar archivo: {e}")

    def login_institucional(self, correo, password):
        try:
            google_btn = self.wait.until(
                EC.element_to_be_clickable((By.ID, "btn-google"))
            )
            google_btn.click()
            print(" Click en 'Iniciar sesión con Google'")
            self.driver.switch_to.window(self.driver.window_handles[-1])
            human_wait(3, 6)

            try:
                email_input = self.wait.until(
                    EC.presence_of_element_located((By.ID, "identifierId"))
                )
                email_input.send_keys(correo)
                email_input.send_keys(u'\ue007')
                print(" Correo ingresado")
                human_wait(2, 4)
            except:
                print(" No pidió correo.")

            try:
                password_input = self.wait_long.until(
                    EC.presence_of_element_located((By.NAME, "Passwd"))
                )
                password_input.send_keys(password)
                password_input.send_keys(u'\ue007')
                print(" Contraseña ingresada")
                human_wait(2, 5)
            except:
                print(" No pidió contraseña.")

            self.wait_long.until(EC.url_contains("sciencedirect.com"))
            print(" Login exitoso, ahora en ScienceDirect")

        except Exception as e:
            print(f" Error durante login institucional: {e}")

    def seleccionar_checkbox(self):
        try:
            self.driver.execute_script("window.scrollTo(0, 0);")
            human_wait(2, 5)

            checkbox = self.wait.until(
                EC.presence_of_element_located((By.ID, "select-all-results"))
            )

            if checkbox.is_selected():
                self.driver.execute_script("arguments[0].click();", checkbox)
                human_wait(1, 2)

            self.driver.execute_script("arguments[0].click();", checkbox)
            print(" Checkbox marcado en esta página.")
            human_wait(2, 4)

        except Exception as e:
            print(f" Error al seleccionar checkbox: {e}")

    def exportar_bibtex(self):
        try:
            self.driver.execute_script("window.scrollTo(0, 0);")
            human_wait(2, 5)

            export_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.export-all-link-button"))
            )
            ActionChains(self.driver).move_to_element(export_btn).perform()
            self.driver.execute_script("arguments[0].click();", export_btn)
            print(" Menú Export abierto.")
            human_wait(2, 4)

            bibtex_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-aa-button='srp-export-multi-bibtex']"))
            )
            self.driver.execute_script("arguments[0].click();", bibtex_btn)
            print(" Exportación a BibTeX lanzada.")

            self.esperar_descarga()
            human_wait(3, 6)

        except Exception as e:
            print(f" No se pudo exportar a BibTeX: {e}")

    def ir_a_siguiente_pagina(self, page_num):
        try:
            siguiente = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[@data-aa-name='srp-next-page']"))
            )
            self.driver.execute_script("arguments[0].click();", siguiente)
            print(" Pasando a la siguiente página")
            self.esperar_overlay()

            # Scroll humano después de cargar la página
            random_scroll(self.driver)

            # Pausa especial cada 20 páginas
            if page_num % 20 == 0:
                print(" Descanso largo para evitar bloqueos...")
                human_wait(120, 300)  # 2 a 5 minutos
            else:
                human_wait(8, 18)  # pausas normales más largas

            return True
        except:
            print(" No hay más páginas disponibles.")
            return False

    def abrir_base_datos(self, query, correo, password, max_paginas=2):
        self.driver.get("https://library.uniquindio.edu.co/databases")
        self.esperar_overlay()

        self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "BASES DATOS x FACULTAD"))
        ).click()
        self.esperar_overlay()

        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-content-listing-item='fac-ingenier-a']"))
        ).click()
        self.esperar_overlay()

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        human_wait(2, 4)

        enlaces = self.wait_long.until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[@href]"))
        )

        enlace_sciencedirect = None
        for enlace in enlaces:
            href = enlace.get_attribute("href")
            if href and "sciencedirect.com" in href:
                enlace_sciencedirect = enlace
                break

        if not enlace_sciencedirect:
            raise Exception(" No se encontró el enlace de ScienceDirect en la página")

        self.driver.execute_script("arguments[0].click();", enlace_sciencedirect)
        print(" Click en ScienceDirect (Descubridor)")

        self.driver.switch_to.window(self.driver.window_handles[-1])
        print(" Cambiado a pestaña de proxy UQ")

        self.login_institucional(correo, password)
        self.aceptar_cookies()

        try:
            search_box = self.wait_long.until(
                EC.presence_of_element_located((By.ID, "qs"))
            )
            search_box.clear()
            search_box.send_keys(query)

            search_btn = self.wait_long.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.button-primary"))
            )
            search_btn.click()
            print(f" Búsqueda lanzada en ScienceDirect: {query}")
            human_wait(4, 7)

            for i in range(1, max_paginas + 1):
                if i > 1:
                    if not self.ir_a_siguiente_pagina(i):
                        break

                self.seleccionar_checkbox()
                self.exportar_bibtex()
                self.renombrar_descarga(i)

        except Exception as e:
            print(f" Error en búsqueda o exportación: {e}")

    def cerrar(self):
        try:
            self.driver.quit()
        except:
            pass


if __name__ == "__main__":
    bot = ScienceDirectDescarga()
    bot.abrir_base_datos(
        query="\"generative artificial intelligence\"",
        correo="jfdiazb@uqvirtual.edu.co",
        password="Lily1007",
        max_paginas=172
    )
    human_wait(5, 10)
    bot.cerrar()
