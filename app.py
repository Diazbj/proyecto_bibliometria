from flask import Flask, send_from_directory, url_for
import os

app = Flask(__name__)

# El directorio donde se encuentran los reportes generados durante el build.
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')

@app.route('/')
def index():
    """
    Muestra una página con enlaces a los reportes generados.
    Los reportes se asume que ya existen, creados durante el paso de build.
    """
    try:
        # Lista los archivos en el directorio de outputs para generar los enlaces.
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
            body {{ font-family: sans-serif; margin: 2em; background-color: #f4f4f9; color: #333; }}
            h1 {{ color: #444; }}
            ul {{ list-style-type: none; padding: 0; }}
            li {{ margin: 0.5em 0; }}
            a {{ 
                text-decoration: none; 
                color: #007BFF;
                background-color: #fff;
                padding: 10px 15px;
                border-radius: 5px;
                border: 1px solid #ddd;
                display: block;
                transition: background-color 0.3s, box-shadow 0.3s;
            }}
            a:hover {{
                background-color: #f8f9fa;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
        </style>
    </head>
    <body>
        <h1>Proyecto Bibliometría</h1>
        <p>Los siguientes reportes de análisis han sido generados:</p>
        <ul>
            {file_links if files else "<li>No se encontraron reportes. El proceso de build puede haber fallado.</li>"}
        </ul>
    </body>
    </html>
    """

@app.route('/outputs/<path:filename>')
def serve_output(filename):
    """Sirve los archivos estáticos (reportes) desde el directorio de outputs."""
    return send_from_directory(OUTPUT_DIR, filename)

if __name__ == '__main__':
    # Este bloque solo se usa para pruebas locales.
    # En producción, Render usa Gunicorn para ejecutar la aplicación.
    app.run(host='0.0.0.0', port=5000, debug=True)


