import re
import time

# -------------------------------
# Algoritmo Quick Sort
# -------------------------------

def partition(arr, low, high):
    """Función de partición para QuickSort"""
    pivot = arr[high][0]  # usamos la clave (year, title) como pivote
    i = low - 1
    for j in range(low, high):
        if arr[j][0] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort(arr, low, high):
    """QuickSort recursivo"""
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)


def quicksort_wrapper(arr):
    """Función envolvente para simplificar llamada"""
    quick_sort(arr, 0, len(arr) - 1)
    return arr


# -------------------------------
# Funciones para trabajar con .bib
# -------------------------------

def extraer_datos(entrada):
    """Extrae (año, título) de una entrada .bib"""
    year_match = re.search(r'year\s*=\s*{?(\d{4})}?', entrada, flags=re.IGNORECASE)
    # usamos ^title para evitar booktitle
    title_match = re.search(r'(?m)^\s*title\s*=\s*{(.+?)}',
                            entrada, flags=re.DOTALL | re.IGNORECASE)

    year = int(year_match.group(1)) if year_match else 9999
    title = title_match.group(1).strip() if title_match else ""
    return (year, title.lower())


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

    # Preprocesar claves (key, entrada)
    entradas_con_clave = [(extraer_datos(e), e) for e in entradas]

    # Ordenar con QuickSort
    start_time = time.perf_counter()
    quicksort_wrapper(entradas_con_clave)
    entradas_ordenadas = [e for _, e in entradas_con_clave]
    end_time = time.perf_counter()

    # Guardar archivo ordenado
    with open("articulos_ordenados_quickSort.bib", "w", encoding="utf-8") as f:
        for e in entradas_ordenadas:
            f.write(e + "\n\n")

    # Reporte
    print("Ordenamiento completado con QuickSort ")
    print(f"Total entradas: {len(entradas_ordenadas)}")
    print(f"Tiempo: {end_time - start_time:.6f} segundos")

