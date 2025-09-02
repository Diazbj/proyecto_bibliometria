import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import glob
import shutil
import tempfile


class ScienceDirectDescarga():
    def __init__(self):
        # Carpeta base de descargas en tu proyecto
        base_dir = r"C:\Users\DiazJ\PycharmProjects\ProyectoAnalisisAlgoritmo\proyecto_bibliometria\descargas"

        # Subcarpeta descargaScienceDirect dentro de esa ruta
        self.download_dir = os.path.join(base_dir, "descargaScienceDirect")
        os.makedirs(self.download_dir, exist_ok=True)

        # Configuración Chrome
        tmp_profile = tempfile.mkdtemp()  # perfil temporal
        options = uc.ChromeOptions()

        options.add_argument(f"--user-data-dir={tmp_profile}")
        options.add_argument("--profile-directory=Default")

        # 🔑 Desactivar sincronización de cuenta y popup de acceso
        options.add_argument("--disable-features=AccountConsistency")
        options.add_argument("--disable-features=ChromeWhatsNewUI")
        options.add_argument("--disable-features=SignInProfileCreation")
        options.add_argument("--disable-features=SigninFrameSignInFlow")
        options.add_argument("--disable-features=EnableEphemeralGuestProfilesOnDesktop")
        options.add_argument("--disable-sync")
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")

        # Configurar descargas automáticas
        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)

        # Abrir Chrome con las opciones configuradas
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
            print("🍪 Cookies aceptadas.")
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
            time.sleep(1)

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
                print(f"📂 Archivo renombrado a {new_name}")
            except Exception as e:
                print(f"⚠️ Error al renombrar archivo: {e}")

    def login_institucional(self, correo, password):
        """Hace login institucional con Google en el proxy UQ"""
        try:
            google_btn = self.wait.until(
                EC.element_to_be_clickable((By.ID, "btn-google"))
            )
            google_btn.click()
            print("✅ Click en 'Iniciar sesión con Google'")

            self.driver.switch_to.window(self.driver.window_handles[-1])

            try:
                email_input = self.wait.until(
                    EC.presence_of_element_located((By.ID, "identifierId"))
                )
                email_input.send_keys(correo)
                email_input.send_keys(u'\ue007')
                print("📧 Correo ingresado")
            except:
                print("ℹ️ No pidió correo.")

            try:
                password_input = self.wait_long.until(
                    EC.presence_of_element_located((By.NAME, "Passwd"))
                )
                time.sleep(1)
                password_input.send_keys(password)
                password_input.send_keys(u'\ue007')
                print("🔑 Contraseña ingresada")
            except:
                print("ℹ️ No pidió contraseña.")

            self.wait_long.until(EC.url_contains("sciencedirect.com"))
            print("🚀 Login exitoso, ahora en ScienceDirect")

        except Exception as e:
            print(f"⚠️ Error durante login institucional: {e}")

    def seleccionar_checkbox(self):
        """Selecciona la casilla de verificación <span class='checkbox-check'>"""
        try:
            label = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='select-all-results']"))
            )
            label.click()
            print("✅ Checkbox seleccionado correctamente.")
        except Exception as e:
            print(f"⚠️ No se pudo seleccionar el checkbox con label: {e}")
            try:
                checkbox = self.driver.find_element(By.ID, "select-all-results")
                self.driver.execute_script("arguments[0].click();", checkbox)
                print("✅ Checkbox forzado con JS.")
            except Exception as e2:
                print(f"❌ Falló también con JS: {e2}")

    def exportar_bibtex(self):
        """Hace clic en Export y luego en Export citation to BibTeX"""
        try:
            # Clic en el botón Export
            export_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.export-all-link-button"))
            )
            export_btn.click()
            print("📤 Menú Export abierto.")

            # Clic en el botón Export citation to BibTeX
            bibtex_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-aa-button='srp-export-multi-bibtex']"))
            )
            bibtex_btn.click()
            print("📂 Exportación a BibTeX lanzada.")

            # Esperamos a que la descarga se complete
            self.esperar_descarga()

        except Exception as e:
            print(f"⚠️ No se pudo exportar a BibTeX: {e}")

    def abrir_base_datos(self, query, correo, password):
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
        time.sleep(2)

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
            raise Exception("❌ No se encontró el enlace de ScienceDirect en la página")

        self.driver.execute_script("arguments[0].click();", enlace_sciencedirect)
        print("🔗 Click en ScienceDirect (Descubridor)")

        self.driver.switch_to.window(self.driver.window_handles[-1])
        print("✅ Cambiado a pestaña de proxy UQ")

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

            print(f"🔎 Búsqueda lanzada en ScienceDirect: {query}")

            # ✅ Seleccionamos el checkbox
            self.seleccionar_checkbox()

            # ✅ Exportamos a BibTeX
            self.exportar_bibtex()

        except Exception as e:
            print(f"⚠️ No se encontró el cuadro de búsqueda: {e}")

    def cerrar(self):
        """Cerrar navegador de forma segura"""
        try:
            self.driver.quit()
        except:
            pass


if __name__ == "__main__":
    bot = ScienceDirectDescarga()
    bot.abrir_base_datos(
        query="\"generative artificial intelligence\"",
        correo="jfdiazb@uqvirtual.edu.co",
        password="Lily1007"
    )
    time.sleep(60)
    bot.cerrar()
