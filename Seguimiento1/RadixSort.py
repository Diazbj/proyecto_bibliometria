import re
import time

# -------------------------------
# Counting Sort auxiliar para Radix Sort
# -------------------------------

def counting_sort(arr, exp):
    """Counting Sort estable aplicado a un dígito específico (exp)"""
    n = len(arr)
    output = [None] * n
    count = [0] * 10

    # Contar ocurrencias del dígito
    for i in range(n):
        year = arr[i][0][0]  # usamos el año como clave principal
        index = (year // exp) % 10
        count[index] += 1

    # Acumular conteos
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Construir salida (estable)
    i = n - 1
    while i >= 0:
        year = arr[i][0][0]
        index = (year // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
        i -= 1

    # Copiar de vuelta
    for i in range(n):
        arr[i] = output[i]


# -------------------------------
# Radix Sort principal
# -------------------------------

def radix_sort(arr):
    """Radix Sort usando Counting Sort en base al año"""
    if not arr:
        return arr

    # Encontrar el máximo año
    max_year = max(k[0] for k, _ in arr)

    # Ordenar por cada dígito del año
    exp = 1
    while max_year // exp > 0:
        counting_sort(arr, exp)
        exp *= 10

    # 🔹 Dentro de los mismos años, ordenar por título
    arr.sort(key=lambda x: (x[0][0], x[0][1]))


# -------------------------------
# Funciones para trabajar con .bib
# -------------------------------

def extraer_datos(entrada):
    """Extrae (año, título) como clave de ordenamiento"""
    year_match = re.search(r'year\s*=\s*{?(\d{4})}?', entrada, flags=re.IGNORECASE)
    title_match = re.search(r'(?m)^\s*title\s*=\s*{(.+?)}',
                            entrada, flags=re.DOTALL | re.IGNORECASE)

    year = int(year_match.group(1)) if year_match else 9999
    title = title_match.group(1).strip().lower() if title_match else ""
    return (year, title)


# -------------------------------
# Parte principal
# -------------------------------
if __name__ == "__main__":
    # Leer archivo .bib
    with open("articulos_con_titulo_y_abstract.bib", "r", encoding="utf-8") as f:
        contenido = f.read()

    # Separar entradas .bib
    entradas = re.split(r'(?=@\w+{)', contenido, flags=re.MULTILINE)
    entradas = [e.strip() for e in entradas if e.strip()]

    # Preprocesar claves (año, título)
    entradas_con_clave = [(extraer_datos(e), e) for e in entradas]

    # Ordenar con Radix Sort
    start_time = time.perf_counter()
    radix_sort(entradas_con_clave)
    end_time = time.perf_counter()

    # Extraer artículos ordenados
    entradas_ordenadas = [e for _, e in entradas_con_clave]

    # Guardar archivo ordenado
    with open("articulos_ordenados_radixSort.bib", "w", encoding="utf-8") as f:
        for e in entradas_ordenadas:
            f.write(e + "\n\n")

    # Reporte
    print("Ordenamiento completado con Radix Sort ✅")
    print(f"Total entradas: {len(entradas_ordenadas)}")
    print(f"Tiempo: {end_time - start_time:.6f} segundos")
    print("Complejidad teórica Radix Sort: O(d·(n + k))")
