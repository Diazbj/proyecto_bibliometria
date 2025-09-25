import re
import time

# -------------------------------
# Algoritmo Gnome Sort
# -------------------------------
def gnome_sort(arr):
    """Ordena usando Gnome Sort adaptado a (clave, entrada)"""
    index = 0
    n = len(arr)
    while index < n:
        if index == 0:
            index += 1
        if arr[index][0] >= arr[index - 1][0]:
            index += 1
        else:
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            index -= 1


# -------------------------------
# Funciones para trabajar con .bib
# -------------------------------
def extraer_datos(entrada):
    """Extrae la clave (año, título) de una entrada .bib"""
    year_match = re.search(r'year\s*=\s*{(\d+)}', entrada, flags=re.IGNORECASE)
    title_match = re.search(r'(?m)^\s*title\s*=\s*{(.+?)}',
                            entrada, flags=re.DOTALL | re.IGNORECASE)

    year = int(year_match.group(1)) if year_match else 9999
    title = title_match.group(1).strip().lower() if title_match else ""
    return (year, title)


# -------------------------------
# Parte principal
# -------------------------------
if __name__ == "__main__":
    # Leer archivo de entrada (.bib)
    with open("articulos_con_titulo_y_abstract.bib", "r", encoding="utf-8") as f:
        contenido = f.read()

    # Separar entradas en bruto
    entradas = re.split(r'(?=@\w+{)', contenido, flags=re.MULTILINE)
    entradas = [e.strip() for e in entradas if e.strip()]

    # Preprocesar entradas con clave (año, título)
    entradas_con_clave = [(extraer_datos(e), e) for e in entradas]

    # Ordenar con Gnome Sort
    start_time = time.perf_counter()
    gnome_sort(entradas_con_clave)
    end_time = time.perf_counter()

    # Recuperar solo las entradas ordenadas
    entradas_ordenadas = [e for _, e in entradas_con_clave]

    # Guardar resultado en archivo
    with open("articulos_ordenados_gnomeSort.bib", "w", encoding="utf-8") as f:
        for e in entradas_ordenadas:
            f.write(e + "\n\n")

    # Reporte final
    print("Ordenamiento completado con Gnome Sort")
    print(f"Total entradas: {len(entradas_ordenadas)}")
    print(f"Tiempo: {end_time - start_time:.6f} segundos")
