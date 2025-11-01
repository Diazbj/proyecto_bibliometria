import os
import bibtexparser

def concat_bib_files(folders, output_file):
    """Concatena todos los archivos .bib de varias carpetas en un único archivo"""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as outfile:
        for folder in folders:
            for filename in os.listdir(folder):
                if filename.endswith(".bib"):
                    filepath = os.path.join(folder, filename)
                    with open(filepath, "r", encoding="utf-8") as infile:
                        outfile.write(infile.read() + "\n")
    print(f" Archivos de {folders} concatenados en {output_file}")


def remove_duplicates(input_file, output_unique, output_duplicates, key="title"):
    """Elimina duplicados en base al campo 'title' o 'doi' y guarda también los duplicados"""
    with open(input_file, encoding="utf-8") as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    seen = set()
    unique_entries = []
    duplicate_entries = []

    for entry in bib_database.entries:
        # Normalizamos: quitamos espacios y pasamos a minúsculas
        value = entry.get(key, "").strip().lower()

        if value:
            if value not in seen:
                seen.add(value)
                unique_entries.append(entry)
            else:
                duplicate_entries.append(entry)

    # Guardamos los únicos
    db_unique = bibtexparser.bibdatabase.BibDatabase()
    db_unique.entries = unique_entries

    writer = bibtexparser.bwriter.BibTexWriter()
    with open(output_unique, "w", encoding="utf-8") as f:
        f.write(writer.write(db_unique))

    # Guardamos los duplicados
    if duplicate_entries:
        db_duplicates = bibtexparser.bibdatabase.BibDatabase()
        db_duplicates.entries = duplicate_entries
        with open(output_duplicates, "w", encoding="utf-8") as f:
            f.write(writer.write(db_duplicates))

    print(f" {len(unique_entries)} artículos únicos guardados en {output_unique}")
    print(f" {len(duplicate_entries)} duplicados guardados en {output_duplicates}")


if __name__ == "__main__":
    # Ajusta rutas
    acm_folder = "archivos/descargaACM"
    sd_folder = "archivos/descargaScienceDirect"

    all_raw = "archivos/todos_raw.bib"
    final_clean = "archivos/articulos_unicos.bib"
    duplicates_file = "archivos/duplicados.bib"

    # Paso 1: concatenar todo
    concat_bib_files([acm_folder, sd_folder], all_raw)

    # Paso 2: eliminar duplicados entre ACM y ScienceDirect
    remove_duplicates(all_raw, final_clean, duplicates_file, key="title")
    # Si tus registros tienen DOI, mejor usar:
    # remove_duplicates(all_raw, final_clean, duplicates_file, key="doi")
