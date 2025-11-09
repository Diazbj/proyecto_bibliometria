import subprocess
import sys
import os
import time


def run_script(script_name, interactive=False):
    """Ejecuta un script Python, capturando su salida o permitiendo interacción."""
    try:
        print(f"\n--- Ejecutando {os.path.basename(script_name)} ---")
        
        # Para scripts interactivos, no capturamos la salida para permitir la entrada del usuario.
        if interactive:
            # Usamos check=True para que falle si el script da un error.
            subprocess.run(
                [sys.executable, script_name],
                check=True,
                encoding="utf-8"
            )
        else:
            # Para scripts no interactivos, capturamos la salida para un log más limpio.
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
        # Si el script falla, su salida de error (si se capturó) estará en e.stderr
        print(f"Error al ejecutar el script {os.path.basename(script_name)}:")
        # Si no se capturó la salida, e.stderr será None, por lo que no imprimimos nada.
        if e.stderr:
            print(e.stderr)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {script_name}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Lista de todos los scripts a ejecutar en orden
    scripts_a_ejecutar = [
        "requerimiento1.py",
        "verificar2.py",
        "requerimiento2.py", # Este es el script interactivo
        "requerimiento3.py",
        "requerimiento4.py",
        "requerimiento5.py"
    ]

    print("--- INICIANDO EJECUCIÓN COMPLETA DEL PROYECTO ---")
    print("El proceso se detendrá en el Requerimiento 2 para solicitar tu entrada.")

    for script_file in scripts_a_ejecutar:
        script_path = os.path.join(base_dir, script_file)
        
        # Determinamos si el script es interactivo
        es_interactivo = (script_file == "requerimiento2.py")
        
        run_script(script_path, interactive=es_interactivo)
        
        # Pequeña pausa entre scripts
        time.sleep(2)

    print("\n--- EJECUCIÓN COMPLETA TERMINADA ---")
