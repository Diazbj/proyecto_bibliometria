import re
import time

# -------------------------------
# Funciones auxiliares
# -------------------------------

def extraer_year(entrada):
    """Extrae el año de una entrada .bib (9999 si no existe)."""
    year_match = re.search(r'year\s*=\s*{?(\d{4})}?', entrada, flags=re.IGNORECASE)
    return int(year_match.group(1)) if year_match else 9999

def extraer_titulo(entrada):
    """Extrae el título de una entrada .bib ('' si no existe)."""
    title_match = re.search(r'(?m)^\s*title\s*=\s*{(.+?)}',
                            entrada, flags=re.DOTALL | re.IGNORECASE)
    return title_match.group(1).strip().lower() if title_match else ""

def comparar(e1, e2):
    """
    Compara dos entradas según:
    1️⃣ Año ascendente
    2️⃣ Título ascendente
    Retorna True si e1 > e2 (para construir un max-heap)
    """
    year1, year2 = extraer_year(e1), extraer_year(e2)
    if year1 != year2:
        return year1 > year2
    return extraer_titulo(e1) > extraer_titulo(e2)

# -------------------------------
# Algoritmo HeapSort (fiel al original)
# -------------------------------

def heapify(arr, n, i):
    """Asegura la propiedad de heap máximo según (año, título)."""
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and comparar(arr[l], arr[largest]):
        largest = l
    if r < n and comparar(arr[r], arr[largest]):
        largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    """HeapSort que ordena por año y luego título (ascendente)."""
    n = len(arr)

    # 1️⃣ Construir max-heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # 2️⃣ Extraer elementos uno por uno
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)

# -------------------------------
# Parte principal
# -------------------------------
if __name__ == "__main__":
    # Leer archivo .bib
    with open("articulos_con_titulo_y_abstract.bib", "r", encoding="utf-8") as f:
        contenido = f.read()

    # Separar entradas .bib
    entradas = re.split(r'(?=@\w+{)', contenido, flags=re.MULTILINE)
    entradas = [e.strip() for e in entradas if e.strip()]

    # Ordenar con HeapSort (fiel al algoritmo)
    start_time = time.perf_counter()
    heap_sort(entradas)
    end_time = time.perf_counter()

    # Guardar archivo ordenado
    with open("articulos_ordenados_heapSort.bib", "w", encoding="utf-8") as f:
        for e in entradas:
            f.write(e + "\n\n")

    # Reporte
    print("✅ Ordenamiento completado con HeapSort (fiel al algoritmo)")
    print(f"📚 Total entradas: {len(entradas)}")
    print(f"⏱ Tiempo: {end_time - start_time:.6f} segundos")
