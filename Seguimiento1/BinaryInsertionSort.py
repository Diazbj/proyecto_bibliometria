import re
import time
import bisect

# -------------------------------
# Funciones de comparación
# -------------------------------

def obtener_criterio(entrada):
    """Devuelve (año, título) de la entrada .bib para la comparación"""
    year_match = re.search(r'year\s*=\s*{?(\d{4})}?', entrada, flags=re.IGNORECASE)
    title_match = re.search(r'(?m)^\s*title\s*=\s*{(.+?)}', entrada, flags=re.DOTALL | re.IGNORECASE)

    year = int(year_match.group(1)) if year_match else 9999
    title = title_match.group(1).strip().lower() if title_match else ""
    return (year, title)


def comparar(e1, e2):
    """True si e1 > e2 (usado para orden ascendente por año y luego título)"""
    y1, t1 = obtener_criterio(e1)
    y2, t2 = obtener_criterio(e2)
    if y1 != y2:
        return y1 > y2
    return t1 > t2


# -------------------------------
# Algoritmo Binary Insertion Sort (puro)
# -------------------------------

def binary_insertion_sort(arr):
    """Ordena directamente las entradas usando Binary Insertion Sort puro"""
    for i in range(1, len(arr)):
        key = arr[i]
        # Búsqueda binaria manual (para mantener el algoritmo fiel)
        low, high = 0, i
        while low < high:
            mid = (low + high) // 2
            if comparar(arr[mid], key):  # si arr[mid] > key
                high = mid
            else:
                low = mid + 1
        # Insertar key en la posición encontrada
        arr = arr[:low] + [key] + arr[low:i] + arr[i+1:]
    return arr


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

    # Ordenar con Binary Insertion Sort puro
    start_time = time.perf_counter()
    entradas_ordenadas = binary_insertion_sort(entradas)
    end_time = time.perf_counter()

    # Guardar archivo ordenado
    with open("articulos_ordenados_binaryInsertionSort.bib", "w", encoding="utf-8") as f:
        for e in entradas_ordenadas:
            f.write(e + "\n\n")

    # Reporte
    print(" Ordenamiento completado con Binary Insertion Sort (versión pura)")
    print(f" Total entradas: {len(entradas_ordenadas)}")
    print(f"Tiempo: {end_time - start_time:.6f} segundos")
