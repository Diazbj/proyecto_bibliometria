import re
import time

# -------------------------------
# Pigeonhole Sort
# -------------------------------
def pigeonholeSort(arr, key=lambda x: x):
    if not arr:
        return

    # Calcular min y max
    valores = [key(e)[0] for e in arr]  # usamos el año como primera clave
    min_val = min(valores)
    max_val = max(valores)

    rango = max_val - min_val + 1
    holes = [[] for _ in range(rango)]

    # Colocar entradas en sus "casillas" según el año
    for e in arr:
        year, title = key(e)
        holes[year - min_val].append(e)

    # Reconstruir lista ordenada
    arr.clear()
    for bucket in holes:
        # ordenar dentro del bucket por título
        bucket.sort(key=lambda e: key(e)[1])
        arr.extend(bucket)


# -------------------------------
# Extraer datos de entrada .bib
# -------------------------------
def extraer_datos(entrada):
    year_match = re.search(r'year\s*=\s*[{"](\d+)[}"]', entrada)
    title_match = re.search(r'(?m)^\s*title\s*=\s*[{"](.+?)[}"]', entrada, flags=re.DOTALL)
    year = int(year_match.group(1)) if year_match else 9999
    title = title_match.group(1).strip() if title_match else ""
    return (year, title)


# -------------------------------
# Parte principal
# -------------------------------
if __name__ == "__main__":
    # Leer archivo
    with open("articulos_con_titulo_y_abstract.bib", "r", encoding="utf-8") as f:
        contenido = f.read()

    # Separar entradas .bib
    entradas = re.split(r'(?=@\w+{)', contenido, flags=re.MULTILINE)
    entradas = [e.strip() for e in entradas if e.strip()]

    # Ordenar con Pigeonhole Sort
    start_time = time.perf_counter()
    pigeonholeSort(entradas, key=lambda e: extraer_datos(e))
    end_time = time.perf_counter()

    # Guardar archivo ordenado
    with open("articulos_ordenados_pigeonholeSort.bib", "w", encoding="utf-8") as f:
        for e in entradas:
            f.write(e + "\n\n")

    # Reporte
    print("Ordenamiento completado con Pigeonhole Sort ")
    print(f"Total entradas: {len(entradas)}")
    print(f"Tiempo: {end_time - start_time:.6f} segundos")
