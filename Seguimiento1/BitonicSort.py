import re
import time

# -------------------------------
# Funciones de comparación
# -------------------------------
def obtener_criterio(entrada):
    """Devuelve (año, título) de la entrada para comparar"""
    year_match = re.search(r'year\s*=\s*{?(\d{4})}?', entrada, flags=re.IGNORECASE)
    title_match = re.search(r'(?m)^\s*title\s*=\s*{(.+?)}', entrada, flags=re.DOTALL | re.IGNORECASE)

    year = int(year_match.group(1)) if year_match else 9999
    title = title_match.group(1).strip().lower() if title_match else ""
    return (year, title)

def comparar(e1, e2):
    """Devuelve True si e1 > e2 según año y título"""
    y1, t1 = obtener_criterio(e1)
    y2, t2 = obtener_criterio(e2)
    if y1 != y2:
        return y1 > y2
    return t1 > t2

# -------------------------------
# Algoritmo Bitonic Sort puro
# -------------------------------
def comp_and_swap(arr, i, j, dire):
    if (dire == 1 and comparar(arr[i], arr[j])) or (dire == 0 and comparar(arr[j], arr[i])):
        arr[i], arr[j] = arr[j], arr[i]

def bitonic_merge(arr, low, cnt, dire):
    if cnt > 1:
        k = cnt // 2
        for i in range(low, low + k):
            comp_and_swap(arr, i, i + k, dire)
        bitonic_merge(arr, low, k, dire)
        bitonic_merge(arr, low + k, k, dire)

def bitonic_sort_rec(arr, low, cnt, dire):
    if cnt > 1:
        k = cnt // 2
        bitonic_sort_rec(arr, low, k, 1)      # ascendente
        bitonic_sort_rec(arr, low + k, k, 0)  # descendente
        bitonic_merge(arr, low, cnt, dire)

def bitonic_sort(arr, up=1):
    bitonic_sort_rec(arr, 0, len(arr), up)
    return arr

# -------------------------------
# Utilidades
# -------------------------------
def siguiente_potencia_de_dos(x):
    """Devuelve la siguiente potencia de 2 >= x"""
    return 1 << (x - 1).bit_length()

# -------------------------------
# Wrapper para usar en Representacion.py
# -------------------------------
def bitonic_sort_wrapper(arr):
    """Envuelve Bitonic Sort para manejar listas no potencia de 2"""
    entradas = arr[:]  # copia para no modificar la original

    # Rellenar hasta potencia de 2
    n = len(entradas)
    m = siguiente_potencia_de_dos(n)
    while len(entradas) < m:
        entradas.append("year = {9999}, title = {zzzzzzzz}")  # marcador

    # Ejecutar Bitonic Sort
    bitonic_sort(entradas, up=1)

    # Eliminar los marcadores
    entradas_ordenadas = [e for e in entradas if "zzzzzzzz" not in e]
    return entradas_ordenadas

# -------------------------------
# Parte principal
# -------------------------------
if __name__ == "__main__":
    with open("articulos_con_titulo_y_abstract.bib", "r", encoding="utf-8") as f:
        contenido = f.read()

    entradas = re.split(r'(?=@\w+{)', contenido, flags=re.MULTILINE)
    entradas = [e.strip() for e in entradas if e.strip()]

    start_time = time.perf_counter()
    entradas_ordenadas = bitonic_sort_wrapper(entradas)
    end_time = time.perf_counter()

    with open("articulos_ordenados_bitonicSort.bib", "w", encoding="utf-8") as f:
        for e in entradas_ordenadas:
            f.write(e + "\n\n")

    print(" Ordenamiento completado con Bitonic Sort (wrapper corregido)")
    print(f" Total entradas: {len(entradas_ordenadas)}")
    print(f" Tiempo: {end_time - start_time:.6f} segundos")
