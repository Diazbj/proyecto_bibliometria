import bibtexparser

def verificar_y_filtrar(input_file, output_validos, output_eliminados):
    """
    Verifica que todos los artículos tengan 'title' y 'abstract'.
    Guarda en output_validos los que cumplen y en output_eliminados los que no.
    """
    with open(input_file, encoding="utf-8") as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    validos = []
    eliminados = []

    for entry in bib_database.entries:
        titulo = entry.get("title", "").strip()
        abstract = entry.get("abstract", "").strip()

        if titulo and abstract:
            validos.append(entry)
        else:
            eliminados.append(entry)

    # Guardar artículos válidos
    db_validos = bibtexparser.bibdatabase.BibDatabase()
    db_validos.entries = validos
    writer = bibtexparser.bwriter.BibTexWriter()
    with open(output_validos, "w", encoding="utf-8") as f:
        f.write(writer.write(db_validos))

    # Guardar artículos eliminados
    if eliminados:
        db_eliminados = bibtexparser.bibdatabase.BibDatabase()
        db_eliminados.entries = eliminados
        with open(output_eliminados, "w", encoding="utf-8") as f:
            f.write(writer.write(db_eliminados))

    print(f" Total de artículos: {len(bib_database.entries)}")
    print(f"Artículos válidos: {len(validos)} → guardados en {output_validos}")
    print(f" Artículos eliminados (sin título o abstract): {len(eliminados)} → guardados en {output_eliminados}")


if __name__ == "__main__":
    # Archivo que quieres verificar
    archivo_bib = "archivos/articulos_unicos.bib"
    archivo_validos = "archivos/articulos_con_titulo_y_abstract.bib"
    archivo_eliminados = "archivos/articulos_eliminados.bib"

    verificar_y_filtrar(archivo_bib, archivo_validos, archivo_eliminados)
