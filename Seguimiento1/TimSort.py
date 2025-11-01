import re
import time

MIN_MERGE = 32

# -------------------------------
# Funciones auxiliares de extracción
# -------------------------------
def extraer_year(entrada):
    match = re.search(r'year\s*=\s*[{"](\d+)[}"]', entrada, flags=re.IGNORECASE)
    return int(match.group(1)) if match else 9999

def extraer_title(entrada):
    match = re.search(r'(?m)^\s*title\s*=\s*[{"](.+?)[}"]', entrada, flags=re.DOTALL | re.IGNORECASE)
    return match.group(1).strip().lower() if match else ""

# -------------------------------
# Comparador fiel por año y título
# -------------------------------
def es_menor_igual(e1, e2):
    y1, y2 = extraer_year(e1), extraer_year(e2)
    t1, t2 = extraer_title(e1), extraer_title(e2)

    if y1 < y2:
        return True
    if y1 == y2 and t1 <= t2:
        return True
    return False

def es_menor(e1, e2):
    y1, y2 = extraer_year(e1), extraer_year(e2)
    t1, t2 = extraer_title(e1), extraer_title(e2)

    if y1 < y2:
        return True
    if y1 == y2 and t1 < t2:
        return True
    return False

# -------------------------------
# TimSort fiel al algoritmo
# -------------------------------
def calcMinRun(n):
    r = 0
    while n >= MIN_MERGE:
        r |= n & 1
        n >>= 1
    return n + r

def insertionSort(arr, left, right):
    for i in range(left + 1, right + 1):
        j = i
        while j > left and es_menor(arr[j], arr[j - 1]):
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            j -= 1

def merge(arr, l, m, r):
    left = arr[l:m + 1]
    right = arr[m + 1:r + 1]

    i = j = 0
    k = l

    while i < len(left) and j < len(right):
        if es_menor_igual(left[i], right[j]):
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1

def timSort(arr):
    n = len(arr)
    minRun = calcMinRun(n)

    # Paso 1: insertion sort en pequeños bloques
    for start in range(0, n, minRun):
        end = min(start + minRun - 1, n - 1)
        insertionSort(arr, start, end)

    # Paso 2: fusionar iterativamente
    size = minRun
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), (n - 1))
            if mid < right:
                merge(arr, left, mid, right)
        size *= 2

# -------------------------------
# Parte principal para .bib
# -------------------------------
if __name__ == "__main__":
    with open("articulos_con_titulo_y_abstract.bib", "r", encoding="utf-8") as f:
        contenido = f.read()

    # Separar entradas .bib
    entradas = re.split(r'(?=@\w+{)', contenido, flags=re.MULTILINE)
    entradas = [e.strip() for e in entradas if e.strip()]

    # Ordenar usando TimSort fiel (sin clave)
    start_time = time.perf_counter()
    timSort(entradas)
    end_time = time.perf_counter()

    # Guardar archivo ordenado
    with open("articulos_ordenados_timSort.bib", "w", encoding="utf-8") as f:
        for e in entradas:
            f.write(e + "\n\n")

    print("Ordenamiento completado con TimSort (fiel, sin clave)")
    print(f" Total entradas: {len(entradas)}")
    print(f" Tiempo: {end_time - start_time:.6f} segundos")
