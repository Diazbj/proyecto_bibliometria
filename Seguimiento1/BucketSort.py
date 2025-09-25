import re
import time

# -------------------------------
# Algoritmo Bucket Sort
# -------------------------------

def insertion_sort_bucket(bucket):
    """Ordena un bucket usando Insertion Sort"""
    for i in range(1, len(bucket)):
        current = bucket[i]
        j = i - 1
        while j >= 0 and bucket[j][0] > current[0]:
            bucket[j + 1] = bucket[j]
            j -= 1
        bucket[j + 1] = current


def bucket_sort(arr):
    """Ordena usando Bucket Sort una lista de (key, entrada)"""
    n = len(arr)
    if n == 0:
        return []

    # Rango de años
    years = [k[0] for k, _ in arr]
    min_year, max_year = min(years), max(years)

    # Inicializar buckets
    buckets = [[] for _ in range(n)]

    # Distribuir entradas en buckets según el año
    for k, entry in arr:
        year = k[0]
        if max_year == min_year:
            idx = 0
        else:
            idx = int((year - min_year) / (max_year - min_year) * (n - 1))
        buckets[idx].append((k, entry))

    # Ordenar cada bucket internamente por (año, título)
    for b in buckets:
        if b:
            insertion_sort_bucket(b)

    # Concatenar resultados
    sorted_list = []
    for b in buckets:
        for _, entry in b:
            sorted_list.append(entry)

    return sorted_list


# -------------------------------
# Funciones para trabajar con .bib
# -------------------------------

def extraer_datos(entrada):
    """Extrae (año, título) de una entrada .bib"""
    year_match = re.search(r'year\s*=\s*{?(\d{4})}?', entrada, flags=re.IGNORECASE)
    # buscamos solo `title =` (no booktitle)
    title_match = re.search(r'(?m)^\s*title\s*=\s*{(.+?)}',
                            entrada, flags=re.DOTALL | re.IGNORECASE)

    year = int(year_match.group(1)) if year_match else 9999
    title = title_match.group(1).strip() if title_match else ""
    return (year, title.lower())


# -------------------------------
# Parte principal
# -------------------------------
if __name__ == "__main__":
    # Leer archivo de entrada .bib
    with open("articulos_con_titulo_y_abstract.bib", "r", encoding="utf-8") as f:
        contenido = f.read()

    # Separar entradas .bib
    entradas = re.split(r'(?=@\w+{)', contenido, flags=re.MULTILINE)
    entradas = [e.strip() for e in entradas if e.strip()]

    # Preprocesar claves (key, entrada)
    entradas_con_clave = [(extraer_datos(e), e) for e in entradas]

    # Ordenar con Bucket Sort
    start_time = time.perf_counter()
    entradas_ordenadas = bucket_sort(entradas_con_clave)
    end_time = time.perf_counter()

    # Guardar archivo ordenado
    with open("articulos_ordenados_bucketSort.bib", "w", encoding="utf-8") as f:
        for e in entradas_ordenadas:
            f.write(e + "\n\n")

    # Reporte
    print("Ordenamiento completado con Bucket Sort ✅")
    print(f"Total entradas: {len(entradas_ordenadas)}")
    print(f"Tiempo: {end_time - start_time:.6f} segundos")
    print("Complejidad teórica Bucket Sort: O(n + k), siendo k el número de buckets")
