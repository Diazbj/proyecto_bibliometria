import re
import time

# -------------------------------
# Funciones auxiliares
# -------------------------------

def extraer_year(entrada):
    """Extrae el año de una entrada .bib (devuelve 9999 si no existe)."""
    year_match = re.search(r'year\s*=\s*[{"](\d+)[}"]', entrada)
    return int(year_match.group(1)) if year_match else 9999

def extraer_titulo(entrada):
    """Extrae el título de una entrada .bib (cadena vacía si no existe)."""
    title_match = re.search(r'(?m)^\s*title\s*=\s*[{"](.+?)[}"]', entrada, flags=re.DOTALL)
    return title_match.group(1).strip().lower() if title_match else ""

# -------------------------------
# Counting Sort para Radix
# -------------------------------

def counting_sort(arr, exp):
    """Counting Sort estable por dígito del año sin usar clave–valor."""
    n = len(arr)
    output = [None] * n
    count = [0] * 10

    # Contar ocurrencias según el dígito actual
    for i in range(n):
        year = extraer_year(arr[i])
        index = (year // exp) % 10
        count[index] += 1

    # Acumular conteos
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Construir salida estable (de atrás hacia adelante)
    i = n - 1
    while i >= 0:
        year = extraer_year(arr[i])
        index = (year // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
        i -= 1

    # Copiar de vuelta al arreglo original
    for i in range(n):
        arr[i] = output[i]

# -------------------------------
# Radix Sort principal
# -------------------------------

def radix_sort(arr):
    """Radix Sort fiel al algoritmo original (solo por año)."""
    if not arr:
        return arr

    # Encontrar el año máximo
    max_year = max(extraer_year(e) for e in arr)

    # Ordenar por cada dígito (LSD -> MSD)
    exp = 1
    while max_year // exp > 0:
        counting_sort(arr, exp)
        exp *= 10

    # Paso adicional: ordenar por título dentro de cada grupo con el mismo año
    i = 0
    while i < len(arr):
        j = i + 1
        while j < len(arr) and extraer_year(arr[j]) == extraer_year(arr[i]):
            j += 1
        # Ordenar el subgrupo [i:j] por título
        arr[i:j] = sorted(arr[i:j], key=extraer_titulo)
        i = j

# -------------------------------
# Parte principal para .bib
# -------------------------------
if __name__ == "__main__":
    #  Leer archivo original
    with open("articulos_con_titulo_y_abstract.bib", "r", encoding="utf-8") as f:
        contenido = f.read()

    #  Separar entradas
    entradas = re.split(r'(?=@\w+{)', contenido, flags=re.MULTILINE)
    entradas = [e.strip() for e in entradas if e.strip()]

    #  Ordenar con Radix Sort
    start_time = time.perf_counter()
    radix_sort(entradas)
    end_time = time.perf_counter()

    #  Guardar archivo ordenado
    with open("articulos_ordenados_radixSort.bib", "w", encoding="utf-8") as f:
        for e in entradas:
            f.write(e + "\n\n")

    #  Reporte
    print(" Ordenamiento completado con Radix Sort (fiel al algoritmo)")
    print(f"Total entradas: {len(entradas)}")
    print(f"️ Tiempo: {end_time - start_time:.6f} segundos")
