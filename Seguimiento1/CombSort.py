import re
import time

# -------------------------------
# Funciones auxiliares
# -------------------------------

def extraer_year(entrada):
    """Extrae el año de una entrada .bib o devuelve 9999 si no existe."""
    match = re.search(r'year\s*=\s*{?(\d{4})}?', entrada, flags=re.IGNORECASE)
    return int(match.group(1)) if match else 9999

def extraer_titulo(entrada):
    """Extrae el título de una entrada .bib o devuelve cadena vacía si no existe."""
    match = re.search(r'(?m)^\s*title\s*=\s*{(.+?)}', entrada, flags=re.DOTALL | re.IGNORECASE)
    return match.group(1).strip().lower() if match else ""

def es_mayor(e1, e2):
    """
    ✅ Devuelve True si e1 > e2 comparando primero por año y luego por título.
    """
    y1, y2 = extraer_year(e1), extraer_year(e2)
    if y1 != y2:
        return y1 > y2
    return extraer_titulo(e1) > extraer_titulo(e2)


# -------------------------------
# Algoritmo Comb Sort (fiel)
# -------------------------------

def getNextGap(gap):
    """Reduce el gap usando el factor de contracción estándar (1.3 aprox)."""
    gap = (gap * 10) // 13
    return 1 if gap < 1 else gap

def comb_sort(arr):
    """Ordena una lista de entradas .bib por año y título usando Comb Sort puro."""
    n = len(arr)
    gap = n
    swapped = True

    while gap != 1 or swapped:
        gap = getNextGap(gap)
        swapped = False

        for i in range(0, n - gap):
            if es_mayor(arr[i], arr[i + gap]):
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swapped = True


# -------------------------------
# Parte principal
# -------------------------------
if __name__ == "__main__":
    # Leer archivo .bib
    with open("articulos_con_titulo_y_abstract.bib", "r", encoding="utf-8") as f:
        contenido = f.read()

    # Separar entradas
    entradas = re.split(r'(?=@\w+{)', contenido, flags=re.MULTILINE)
    entradas = [e.strip() for e in entradas if e.strip()]

    # Ordenar con Comb Sort fiel
    start_time = time.perf_counter()
    comb_sort(entradas)
    end_time = time.perf_counter()

    # Guardar archivo ordenado
    with open("articulos_ordenados_combSort.bib", "w", encoding="utf-8") as f:
        for e in entradas:
            f.write(e + "\n\n")

    # Reporte
    print("✅ Ordenamiento completado con Comb Sort (fiel al algoritmo)")
    print(f"📚 Total entradas: {len(entradas)}")
    print(f"⏱ Tiempo: {end_time - start_time:.6f} segundos")
