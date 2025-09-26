import re
import time

# -------------------------------
# Funciones auxiliares
# -------------------------------

def extraer_year(entrada):
    """Extrae el año de una entrada .bib (retorna 9999 si no existe)."""
    year_match = re.search(r'year\s*=\s*{?(\d{4})}?', entrada, flags=re.IGNORECASE)
    return int(year_match.group(1)) if year_match else 9999

def extraer_titulo(entrada):
    """Extrae el título de una entrada .bib (retorna '' si no existe)."""
    title_match = re.search(r'(?m)^\s*title\s*=\s*{(.+?)}',
                            entrada, flags=re.DOTALL | re.IGNORECASE)
    return title_match.group(1).strip().lower() if title_match else ""

def es_mayor(e1, e2):
    """
    Compara dos entradas:
    ✅ Devuelve True si e1 > e2 según (año, título)
    """
    year1, year2 = extraer_year(e1), extraer_year(e2)
    if year1 != year2:
        return year1 > year2
    return extraer_titulo(e1) > extraer_titulo(e2)


# -------------------------------
# Algoritmo Gnome Sort (fiel al original)
# -------------------------------

def gnome_sort(arr):
    """Ordena la lista de entradas usando Gnome Sort por año y luego título."""
    index = 0
    n = len(arr)
    while index < n:
        if index == 0:
            index += 1
        # Si arr[index - 1] <= arr[index], seguimos avanzando
        elif not es_mayor(arr[index - 1], arr[index]):
            index += 1
        else:
            # Si arr[index - 1] > arr[index], intercambiamos y retrocedemos
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            index -= 1


# -------------------------------
# Parte principal
# -------------------------------
if __name__ == "__main__":
    # Leer archivo de entrada
    with open("articulos_con_titulo_y_abstract.bib", "r", encoding="utf-8") as f:
        contenido = f.read()

    # Separar las entradas .bib
    entradas = re.split(r'(?=@\w+{)', contenido, flags=re.MULTILINE)
    entradas = [e.strip() for e in entradas if e.strip()]

    # Ordenar usando Gnome Sort fiel
    start_time = time.perf_counter()
    gnome_sort(entradas)
    end_time = time.perf_counter()

    # Guardar archivo ordenado
    with open("articulos_ordenados_gnomeSort.bib", "w", encoding="utf-8") as f:
        for e in entradas:
            f.write(e + "\n\n")

    # Reporte final
    print("✅ Ordenamiento completado con Gnome Sort (fiel al algoritmo)")
    print(f"📚 Total entradas: {len(entradas)}")
    print(f"⏱ Tiempo: {end_time - start_time:.6f} segundos")
