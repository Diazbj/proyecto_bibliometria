import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://library.uniquindio.edu.co/databases"

# Navegador oculto
driver = uc.Chrome(headless=True)
wait = WebDriverWait(driver, 30)

try:
    # Abrir página
    driver.get(URL)
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    print("[OK] Página inicial cargada:", driver.current_url)

    # Esperar que desaparezca el overlay de carga
    try:
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "onload-background")))
        print("[OK] Overlay de carga eliminado.")
    except:
        print("[WARN] No se encontró overlay o ya estaba oculto.")

    # Clic en "BASES DATOS x FACULTAD"
    link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "BASES DATOS x FACULTAD")))
    link.click()
    print("[OK] Se hizo clic en 'BASES DATOS x FACULTAD'.")

except Exception as e:
    print(f"[ERROR] {e}")

finally:
    driver.quit()
    print("[INFO] Navegador cerrado.")
