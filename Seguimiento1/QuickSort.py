import re
import time
import sys

# (Opcional) Aumentar el límite de recursión para archivos grandes
sys.setrecursionlimit(10000)

# -------------------------------
# Funciones auxiliares para extraer datos
# -------------------------------

def extraer_year(entrada):
    """Extrae el año de una entrada .bib (9999 si no existe)."""
    year_match = re.search(r'year\s*=\s*{?(\d{4})}?', entrada, flags=re.IGNORECASE)
    return int(year_match.group(1)) if year_match else 9999

def extraer_titulo(entrada):
    """Extrae el título de una entrada .bib ('' si no existe)."""
    title_match = re.search(r'(?m)^\s*title\s*=\s*{(.+?)}', entrada, flags=re.DOTALL | re.IGNORECASE)
    return title_match.group(1).strip().lower() if title_match else ""

def comparar(e1, e2):
    """
    Devuelve True si e1 <= e2 según:
    - Año ascendente
    - Título ascendente dentro del mismo año
    """
    y1, y2 = extraer_year(e1), extraer_year(e2)
    if y1 < y2:
        return True
    elif y1 > y2:
        return False
    else:
        # Mismo año → comparar título
        return extraer_titulo(e1) <= extraer_titulo(e2)

# -------------------------------
# Algoritmo QuickSort puro
# -------------------------------

def partition(arr, low, high):
    """Función de partición para QuickSort (sin clave–valor)."""
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if comparar(arr[j], pivot):  # comparación directa
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quick_sort(arr, low, high):
    """QuickSort recursivo clásico."""
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

def quicksort_wrapper(arr):
    """Función envolvente para simplificar el uso de QuickSort."""
    quick_sort(arr, 0, len(arr) - 1)
    return arr

# -------------------------------
# Parte principal para .bib
# -------------------------------
if __name__ == "__main__":
    # 1️⃣ Leer archivo original
    with open("articulos_con_titulo_y_abstract.bib", "r", encoding="utf-8") as f:
        contenido = f.read()

    # 2️⃣ Separar entradas
    entradas = re.split(r'(?=@\w+{)', contenido, flags=re.MULTILINE)
    entradas = [e.strip() for e in entradas if e.strip()]

    # 3️⃣ Ordenar directamente con QuickSort puro
    start_time = time.perf_counter()
    quicksort_wrapper(entradas)
    end_time = time.perf_counter()

    # 4️⃣ Guardar archivo ordenado
    with open("articulos_ordenados_quickSort.bib", "w", encoding="utf-8") as f:
        for e in entradas:
            f.write(e + "\n\n")

    # 5️⃣ Reporte
    print("✅ Ordenamiento completado con QuickSort (fiel al algoritmo)")
    print(f"📚 Total entradas: {len(entradas)}")
    print(f"⏱ Tiempo: {end_time - start_time:.6f} segundos")
