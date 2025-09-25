import re
import time

# -------------------------------
# Algoritmo Bitonic Sort
# -------------------------------

def comp_and_swap(arr, i, j, dire):
    """Compara y hace swap según la dirección"""
    if (dire == 1 and arr[i][0] > arr[j][0]) or (dire == 0 and arr[i][0] < arr[j][0]):
        arr[i], arr[j] = arr[j], arr[i]


def bitonic_merge(arr, low, cnt, dire):
    """Fusiona secuencia bitónica en orden creciente o decreciente"""
    if cnt > 1:
        k = cnt // 2
        for i in range(low, low + k):
            comp_and_swap(arr, i, i + k, dire)
        bitonic_merge(arr, low, k, dire)
        bitonic_merge(arr, low + k, k, dire)


def bitonic_sort_rec(arr, low, cnt, dire):
    """QuickSort recursivo"""
    if cnt > 1:
        k = cnt // 2
        # Orden creciente
        bitonic_sort_rec(arr, low, k, 1)
        # Orden decreciente
        bitonic_sort_rec(arr, low + k, k, 0)
        # Mezcla secuencia en orden "dire"
        bitonic_merge(arr, low, cnt, dire)


def bitonic_sort(arr, up=1):
    """Ordena usando Bitonic Sort"""
    n = len(arr)
    bitonic_sort_rec(arr, 0, n, up)
    return arr


# -------------------------------
# Funciones para trabajar con .bib
# -------------------------------

def extraer_datos(entrada):
    """Extrae (año, título) de una entrada .bib"""
    year_match = re.search(r'year\s*=\s*{?(\d{4})}?', entrada, flags=re.IGNORECASE)
    title_match = re.search(r'(?m)^\s*title\s*=\s*{(.+?)}',
                            entrada, flags=re.DOTALL | re.IGNORECASE)

    year = int(year_match.group(1)) if year_match else 9999
    title = title_match.group(1).strip() if title_match else ""
    return (year, title.lower())


def siguiente_potencia_de_dos(x):
    """Devuelve la siguiente potencia de 2 >= x"""
    return 1 << (x - 1).bit_length()


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

    # Preprocesar claves
    entradas_con_clave = [(extraer_datos(e), e) for e in entradas]

    # Rellenar hasta la siguiente potencia de 2
    n = len(entradas_con_clave)
    m = siguiente_potencia_de_dos(n)
    while len(entradas_con_clave) < m:
        entradas_con_clave.append(((9999, "zzzzzzzzzz"), None))  # marcador que quedará al final

    # Ordenar con Bitonic Sort
    start_time = time.perf_counter()
    bitonic_sort(entradas_con_clave, up=1)
    end_time = time.perf_counter()

    # Recuperar eliminando los marcadores
    entradas_ordenadas = [e for _, e in entradas_con_clave if e is not None]

    # Guardar archivo ordenado
    with open("articulos_ordenados_bitonicSort.bib", "w", encoding="utf-8") as f:
        for e in entradas_ordenadas:
            f.write(e + "\n\n")

    # Reporte
    print("Ordenamiento completado con Bitonic Sort ✅")
    print(f"Total entradas: {len(entradas_ordenadas)}")
    print(f"Tiempo: {end_time - start_time:.6f} segundos")
    print("Complejidad teórica Bitonic Sort: O(n log² n)")
