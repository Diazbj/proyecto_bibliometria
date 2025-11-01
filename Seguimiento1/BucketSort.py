import re
import time

# -------------------------------
#  Funciones auxiliares
# -------------------------------

def extraer_year(entrada):
    """Extrae el año de una entrada .bib o devuelve 9999 si no lo encuentra."""
    match = re.search(r'year\s*=\s*{?(\d{4})}?', entrada, flags=re.IGNORECASE)
    return int(match.group(1)) if match else 9999

def extraer_titulo(entrada):
    """Extrae el título de una entrada .bib o devuelve cadena vacía si no lo encuentra."""
    match = re.search(r'(?m)^\s*title\s*=\s*{(.+?)}', entrada, flags=re.DOTALL | re.IGNORECASE)
    return match.group(1).strip().lower() if match else ""

def es_mayor(e1, e2):
    """
     Compara dos entradas .bib devolviendo True si e1 > e2
    según (año ascendente, luego título ascendente).
    """
    y1, y2 = extraer_year(e1), extraer_year(e2)
    if y1 != y2:
        return y1 > y2
    return extraer_titulo(e1) > extraer_titulo(e2)


# -------------------------------
#  Bucket Sort (fiel al algoritmo)
# -------------------------------

def insertion_sort_bucket(bucket):
    """Ordena un bucket con Insertion Sort respetando (año, título)."""
    for i in range(1, len(bucket)):
        current = bucket[i]
        j = i - 1
        while j >= 0 and es_mayor(bucket[j], current):
            bucket[j + 1] = bucket[j]
            j -= 1
        bucket[j + 1] = current

def bucket_sort(arr):
    """Ordena las entradas .bib usando Bucket Sort sin clave–valor."""
    n = len(arr)
    if n == 0:
        return arr

    #  Obtener rango de años
    years = [extraer_year(e) for e in arr]
    min_year, max_year = min(years), max(years)
    rango = max_year - min_year + 1

    #  Crear buckets
    buckets = [[] for _ in range(n)]

    #  Distribuir entradas en buckets según el año
    for entrada in arr:
        year = extraer_year(entrada)
        if max_year == min_year:
            idx = 0
        else:
            idx = int((year - min_year) / (max_year - min_year) * (n - 1))
        buckets[idx].append(entrada)

    #  Ordenar cada bucket con Insertion Sort
    for b in buckets:
        if b:
            insertion_sort_bucket(b)

    # Concatenar resultados
    resultado = []
    for b in buckets:
        resultado.extend(b)

    return resultado


# -------------------------------
#  Parte principal
# -------------------------------
if __name__ == "__main__":
    #  Leer archivo original
    with open("articulos_con_titulo_y_abstract.bib", "r", encoding="utf-8") as f:
        contenido = f.read()

    #  Separar entradas
    entradas = re.split(r'(?=@\w+{)', contenido, flags=re.MULTILINE)
    entradas = [e.strip() for e in entradas if e.strip()]

    #  Ordenar con Bucket Sort fiel
    start_time = time.perf_counter()
    entradas_ordenadas = bucket_sort(entradas)
    end_time = time.perf_counter()

    #  Guardar archivo ordenado
    with open("articulos_ordenados_bucketSort.bib", "w", encoding="utf-8") as f:
        for e in entradas_ordenadas:
            f.write(e + "\n\n")

    #  Reporte final
    print(" Ordenamiento completado con Bucket Sort (fiel al algoritmo)")
    print(f" Total entradas: {len(entradas_ordenadas)}")
    print(f" Tiempo: {end_time - start_time:.6f} segundos")
