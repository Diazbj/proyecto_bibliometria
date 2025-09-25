import re
import time
import bisect

# -------------------------------
# Algoritmo Binary Insertion Sort
# -------------------------------

def binary_insertion_sort(arr):
    """Binary Insertion Sort adaptado a lista de tuplas (clave, entrada)"""
    for i in range(1, len(arr)):
        key_item = arr[i]
        # Usamos bisect para buscar la posición correcta en arr[0:i]
        pos = bisect.bisect_left([x[0] for x in arr[:i]], key_item[0])
        # Insertamos el elemento en la posición encontrada
        arr = arr[:pos] + [key_item] + arr[pos:i] + arr[i+1:]
    return arr


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

    # Ordenar con Binary Insertion Sort
    start_time = time.perf_counter()
    entradas_con_clave = binary_insertion_sort(entradas_con_clave)
    end_time = time.perf_counter()

    # Extraer entradas ordenadas
    entradas_ordenadas = [e for _, e in entradas_con_clave]

    # Guardar archivo ordenado
    with open("articulos_ordenados_binaryInsertionSort.bib", "w", encoding="utf-8") as f:
        for e in entradas_ordenadas:
            f.write(e + "\n\n")

    # Reporte
    print("Ordenamiento completado con Binary Insertion Sort ✅")
    print(f"Total entradas: {len(entradas_ordenadas)}")
    print(f"Tiempo: {end_time - start_time:.6f} segundos")
    print("Complejidad teórica Binary Insertion Sort: O(n²)")
