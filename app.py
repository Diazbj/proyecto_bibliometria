from flask import Flask, jsonify, send_from_directory, url_for
import ejecutar_proyecto
import os
import threading
import time

app = Flask(__name__)

# El directorio donde se guardarán los reportes generados.
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Variable para rastrear el estado del análisis
analysis_status = "No iniciado"
analysis_log = ""

def run_analysis_background():
    """Ejecuta el análisis en segundo plano y actualiza el estado."""
    global analysis_status, analysis_log
    analysis_status = "En progreso..."
    print("Iniciando el análisis en segundo plano...")
    
    # Capturamos la salida estándar para mostrarla en la web
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ejecutar_proyecto.main(output_dir=OUTPUT_DIR)
        analysis_log = captured_output.getvalue()
        analysis_status = "Completado"
        print("Análisis completado con éxito.")
    except Exception as e:
        analysis_log = captured_output.getvalue() + f"\nError durante el análisis: {e}"
        analysis_status = f"Error: {e}"
        print(f"Error durante el análisis: {e}")
    finally:
        sys.stdout = old_stdout

@app.route('/')
def index():
    # Genera dinámicamente la lista de archivos en el directorio de outputs
    try:
        files = [f for f in os.listdir(OUTPUT_DIR) if os.path.isfile(os.path.join(OUTPUT_DIR, f))]
    except FileNotFoundError:
        files = []

    file_links = "".join(
        f'<li><a href="{url_for("serve_output", filename=f)}">{f}</a></li>' for f in sorted(files)
    )

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Proyecto Bibliometría</title>
        <style>
            body {{ font-family: sans-serif; margin: 2em; }}
            h1, h2 {{ color: #333; }}
            a {{ color: #007BFF; }}
            #status {{ padding: 10px; border: 1px solid #ccc; background-color: #f8f9fa; }}
        </style>
    </head>
    <body>
        <h1>Proyecto Bibliometría</h1>
        <p>Bienvenido al panel de control del proyecto de análisis bibliométrico.</p>
        
        <h2>Estado del Análisis</h2>
        <p id="status"><strong>{analysis_status}</strong></p>
        
        <h2>Resultados del Análisis</h2>
        <p>Una vez que el análisis esté 'Completado', los resultados aparecerán aquí:</p>
        <ul>
            {file_links if files else "<li>No hay resultados disponibles. El análisis puede no haber finalizado.</li>"}
        </ul>

        <h2>Registro del Análisis</h2>
        <pre style="background-color: #eee; padding: 10px; border: 1px solid #ccc; max-height: 300px; overflow-y: auto;">{analysis_log or "El registro del análisis aparecerá aquí."}</pre>
    </body>
    </html>
    """

@app.route('/outputs/<path:filename>')
def serve_output(filename):
    return send_from_directory(OUTPUT_DIR, filename)

# Ejecutar el análisis en un hilo separado al iniciar la aplicación
# Esto es crucial para plataformas como Render, que esperan que el servidor web se inicie rápidamente.
analysis_thread = threading.Thread(target=run_analysis_background)
analysis_thread.start()

if __name__ == '__main__':
    # El host '0.0.0.0' hace que el servidor sea accesible en la red local.
    # Render usará gunicorn, por lo que este bloque no se ejecutará en producción.
    app.run(host='0.0.0.0', port=5000, debug=True)

