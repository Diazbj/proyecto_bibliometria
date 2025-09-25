import re
import time

MIN_MERGE = 32

def calcMinRun(n):
    r = 0
    while n >= MIN_MERGE:
        r |= n & 1
        n >>= 1
    return n + r

def insertionSort(arr, left, right, key=lambda x: x):
    for i in range(left + 1, right + 1):
        j = i
        while j > left and key(arr[j]) < key(arr[j - 1]):
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            j -= 1

def merge(arr, l, m, r, key=lambda x: x):
    left = arr[l:m+1]
    right = arr[m+1:r+1]

    i = j = 0
    k = l
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
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

def timSort(arr, key=lambda x: x):
    n = len(arr)
    minRun = calcMinRun(n)

    for start in range(0, n, minRun):
        end = min(start + minRun - 1, n - 1)
        insertionSort(arr, start, end, key)

    size = minRun
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), (n - 1))
            if mid < right:
                merge(arr, left, mid, right, key)
        size = 2 * size


# -------------------------------
# Parte principal para .bib
# -------------------------------
with open("articulos_con_titulo_y_abstract.bib", "r", encoding="utf-8") as f:
    contenido = f.read()

# Separar entradas .bib
entradas = re.split(r'(?=@\w+{)', contenido, flags=re.MULTILINE)

def extraer_datos(entrada):
    year_match = re.search(r'year\s*=\s*{(\d+)}', entrada)
    title_match = re.search(r'title\s*=\s*{(.+?)}', entrada, flags=re.DOTALL)
    year = int(year_match.group(1)) if year_match else 9999
    title = title_match.group(1).strip() if title_match else ""
    return year, title

# Filtrar entradas válidas
entradas = [e.strip() for e in entradas if e.strip()]

# Ordenar usando timSort con clave (year, title)
start_time = time.perf_counter()
timSort(entradas, key=lambda e: extraer_datos(e))
end_time = time.perf_counter()

# Guardar archivo ordenado
with open("articulos_ordenados_timSort.bib", "w", encoding="utf-8") as f:
    for e in entradas:
        f.write(e + "\n\n")

print(f"Ordenamiento completado. Total entradas: {len(entradas)} - Tiempo: {end_time - start_time:.6f} segundos")
