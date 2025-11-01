import subprocess
import sys
import os
import time


def run_script(script_name):
    """Ejecuta un script Python y captura su salida"""
    try:
        print(f"\n Ejecutando {script_name} ...\n")
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8",
            errors="replace"
        )
        print(result.stdout)
        if result.stderr:
            print("Advertencia:\n", result.stderr)
    except subprocess.CalledProcessError as e:
        print(" Error al ejecutar el script:\n", e.stderr)
    except FileNotFoundError:
        print(f" No se encontró el archivo {script_name}")

if __name__ == "__main__":
    # Ruta base del proyecto
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Scripts a ejecutar en orden
    scripts = [
        os.path.join(base_dir, "requerimiento1.py"),  #  script de merge/remove duplicates
        os.path.join(base_dir, "verificar2.py"),      #  script de verificación
    ]

    for script in scripts:
        run_script(script)
        time.sleep(5)

    print("\n Flujo completo terminado")
