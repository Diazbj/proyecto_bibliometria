import os
import re
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase


# -------------------------------------------------------------------
# Paso 1: Concatenar todos los .bib de una carpeta en un archivo único
# -------------------------------------------------------------------
def concat_bib_files(folder, output_file):
    """Concatena todos los archivos .bib de una carpeta en un único archivo"""
    with open(output_file, "w", encoding="utf-8") as outfile:
        for filename in os.listdir(folder):
            if filename.endswith(".bib"):
                filepath = os.path.join(folder, filename)
                with open(filepath, "r", encoding="utf-8") as infile:
                    outfile.write(infile.read() + "\n")
    print(f"📂 Archivos de {folder} concatenados en {output_file}")


# -------------------------------------------------------------------
# Paso 2: Cargar un archivo .bib y convertirlo a lista de entradas
# -------------------------------------------------------------------
def load_bib_file(path):
    """Carga un archivo .bib y devuelve las entradas como lista de diccionarios"""
    with open(path, encoding="utf-8") as bibtex_file:
        return bibtexparser.load(bibtex_file).entries


# -------------------------------------------------------------------
# Paso 3: Normalización de títulos para detectar duplicados
# -------------------------------------------------------------------
def normalize_title(title: str) -> str:
    """Normaliza el título para evitar problemas de comparación"""
    if not title:
        return ""
    title = title.lower().strip()
    title = re.sub(r'\s+', ' ', title)  # espacios múltiples -> uno solo
    return title


# -------------------------------------------------------------------
# Paso 4: Unificación de entradas eliminando duplicados
# -------------------------------------------------------------------
def merge_entries(entries_list):
    """Unifica entradas basadas en el título normalizado"""
    merged = {}
    duplicates = []

    for entry in entries_list:
        key = normalize_title(entry.get("title", ""))

        if key in merged:
            duplicates.append(entry)
            # fusionar información faltante
            for k, v in entry.items():
                if k not in merged[key] or not merged[key][k]:
                    merged[key][k] = v
        else:
            merged[key] = entry
    return list(merged.values()), duplicates


# -------------------------------------------------------------------
# Paso 5: Guardar resultados en archivo .bib
# -------------------------------------------------------------------
def save_bib(entries, filename):
    """Guarda las entradas en un archivo .bib"""
    db = BibDatabase()
    db.entries = entries

    writer = BibTexWriter()
    writer.indent = "    "
    writer.order_entries_by = None  # mantener orden de inserción

    with open(filename, "w", encoding="utf-8") as bibfile:
        bibfile.write(writer.write(db))
    print(f"💾 Guardado {len(entries)} registros en {filename}")


# -------------------------------------------------------------------
# MAIN PIPELINE
# -------------------------------------------------------------------
if __name__ == "__main__":
    # 📂 Rutas de las carpetas de entrada
    acm_folder = "archivos/descargaACM"
    sd_folder = "archivos/descargaScienceDirect"

    # 📂 Archivos concatenados
    acm_raw = "archivos/acm_raw.bib"
    sd_raw = "archivos/sciencedirect_raw.bib"

    # 1️⃣ Concatenar todos los .bib en uno solo por fuente
    concat_bib_files(acm_folder, acm_raw)
    concat_bib_files(sd_folder, sd_raw)

    # 2️⃣ Cargar ambos archivos grandes
    acm_entries = load_bib_file(acm_raw)
    sd_entries = load_bib_file(sd_raw)

    print(f"✅ Cargados: ACM={len(acm_entries)} | SD={len(sd_entries)}")

    # 3️⃣ Unificar y eliminar duplicados
    all_entries = acm_entries + sd_entries
    merged, duplicates = merge_entries(all_entries)

    # 4️⃣ Guardar resultados finales
    save_bib(merged, "archivos/articulos_unificados.bib")
    save_bib(duplicates, "archivos/articulos_duplicados.bib")

    print(f"📊 Resultado final → Unificados: {len(merged)} | Duplicados: {len(duplicates)}")
