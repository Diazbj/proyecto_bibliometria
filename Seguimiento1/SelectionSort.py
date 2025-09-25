import re
import time

# -------------------------------
# Selection Sort optimizado
# -------------------------------
def selectionSort(arr, key=lambda x: x):
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        min_val = key(arr[i])   # cachear valor inicial
        for j in range(i + 1, n):
            val = key(arr[j])
            if val < min_val:
                min_idx = j
                min_val = val
        arr[i], arr[min_idx] = arr[min_idx], arr[i]


# -------------------------------
# Parte principal para .bib
# -------------------------------
with open("articulos_con_titulo_y_abstract.bib", "r", encoding="utf-8") as f:
    contenido = f.read()

# Separar entradas .bib
entradas = re.split(r'(?=@\w+{)', contenido, flags=re.MULTILINE)

def extraer_datos(entrada):
    year_match = re.search(r'year\s*=\s*[{"](\d+)[}"]', entrada)
    title_match = re.search(r'(?m)^\s*title\s*=\s*[{"](.+?)[}"]', entrada, flags=re.DOTALL)
    year = int(year_match.group(1)) if year_match else 9999
    title = title_match.group(1).strip() if title_match else ""
    return (year, title)

# Filtrar entradas válidas
entradas = [e.strip() for e in entradas if e.strip()]

# Preprocesar claves una sola vez
entradas_con_clave = [(extraer_datos(e), e) for e in entradas]

# Ordenar usando Selection Sort con clave precalculada
start_time = time.perf_counter()
selectionSort(entradas_con_clave, key=lambda x: x[0])
end_time = time.perf_counter()

# Recuperar solo las entradas ordenadas
entradas = [e for _, e in entradas_con_clave]

# Guardar archivo ordenado
with open("articulos_ordenados_selectionSort.bib", "w", encoding="utf-8") as f:
    for e in entradas:
        f.write(e + "\n\n")

print("Ordenamiento completado con Selection Sort")
print(f"Total entradas: {len(entradas)}")
print(f"Tiempo: {end_time - start_time:.6f} segundos")
