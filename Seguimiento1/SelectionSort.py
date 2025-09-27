import re
import time

# -------------------------------
# Selection Sort por (año, título)
# -------------------------------
def selectionSort(arr):
    n = len(arr)
    for i in range(n - 1):
        min_idx = i

        # Obtener año y título de la entrada mínima actual
        year_min = extraer_year(arr[min_idx])
        title_min = extraer_title(arr[min_idx])

        for j in range(i + 1, n):
            year_j = extraer_year(arr[j])
            title_j = extraer_title(arr[j])

            # Comparación por año y luego por título
            if (year_j < year_min) or (year_j == year_min and title_j < title_min):
                min_idx = j
                year_min = year_j
                title_min = title_j

        # Intercambiar elementos
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

# -------------------------------
# Funciones auxiliares
# -------------------------------
def extraer_year(entrada):
    match = re.search(r'year\s*=\s*[{"](\d+)[}"]', entrada)
    return int(match.group(1)) if match else 9999  # por defecto un año grande si no lo encuentra

def extraer_title(entrada):
    match = re.search(r'(?m)^\s*title\s*=\s*[{"](.+?)[}"]', entrada, flags=re.DOTALL)
    return match.group(1).strip().lower() if match else ""

# -------------------------------
# Parte principal para .bib
# -------------------------------
with open("articulos_con_titulo_y_abstract.bib", "r", encoding="utf-8") as f:
    contenido = f.read()

# Separar entradas
entradas = re.split(r'(?=@\w+{)', contenido, flags=re.MULTILINE)
entradas = [e.strip() for e in entradas if e.strip()]

# -------------------------------
# Ordenar con Selection Sort fiel
# -------------------------------
start_time = time.perf_counter()
selectionSort(entradas)
end_time = time.perf_counter()

# Guardar archivo ordenado
with open("articulos_ordenados_selectionSort.bib", "w", encoding="utf-8") as f:
    for e in entradas:
        f.write(e + "\n\n")

print(" Ordenamiento completado con Selection Sort (por año y título)")
print(f" Total entradas: {len(entradas)}")
print(f" Tiempo: {end_time - start_time:.6f} segundos")
