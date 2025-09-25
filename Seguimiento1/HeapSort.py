import re
import time

# -------------------------------
# Algoritmo HeapSort
# -------------------------------

def heapify(arr, n, i):
    """Convierte un subárbol en un heap máximo"""
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and arr[l][0] > arr[largest][0]:
        largest = l
    if r < n and arr[r][0] > arr[largest][0]:
        largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heap_sort(arr):
    """HeapSort adaptado a lista de tuplas (clave, entrada)"""
    n = len(arr)

    # Construir heap máximo
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extraer elementos del heap uno por uno
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)


# -------------------------------
# Funciones para trabajar con .bib
# -------------------------------

def extraer_datos(entrada):
    """Extrae (año, título) como clave de ordenamiento"""
    year_match = re.search(r'year\s*=\s*{?(\d{4})}?', entrada, flags=re.IGNORECASE)
    title_match = re.search(r'(?m)^\s*title\s*=\s*{(.+?)}',
                            entrada, flags=re.DOTALL | re.IGNORECASE)

    year = int(year_match.group(1)) if year_match else 9999
    title = title_match.group(1).strip() if title_match else ""
    return (year, title.lower())


# -------------------------------
# Parte principal
# -------------------------------
if __name__ == "__main__":
    # Leer archivo de entrada
    with open("articulos_con_titulo_y_abstract.bib", "r", encoding="utf-8") as f:
        contenido = f.read()

    # Separar entradas .bib
    entradas = re.split(r'(?=@\w+{)', contenido, flags=re.MULTILINE)
    entradas = [e.strip() for e in entradas if e.strip()]

    # Preprocesar claves (year, title)
    entradas_con_clave = [(extraer_datos(e), e) for e in entradas]

    # Ordenar con HeapSort
    start_time = time.perf_counter()
    heap_sort(entradas_con_clave)
    end_time = time.perf_counter()

    # Extraer entradas ordenadas
    entradas_ordenadas = [e for _, e in entradas_con_clave]

    # Guardar archivo ordenado
    with open("articulos_ordenados_heapSort.bib", "w", encoding="utf-8") as f:
        for e in entradas_ordenadas:
            f.write(e + "\n\n")

    # Reporte
    print("Ordenamiento completado con HeapSort")
    print(f"Total entradas: {len(entradas_ordenadas)}")
    print(f"Tiempo: {end_time - start_time:.6f} segundos")
    print("Complejidad teórica HeapSort: O(n log n)")
