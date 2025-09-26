import re
import time

# -------------------------------
# Funciones auxiliares
# -------------------------------
def extraer_year(entrada):
    """Extrae el año de una entrada .bib (9999 si no existe)."""
    year_match = re.search(r'year\s*=\s*{?(\d{4})}?', entrada, flags=re.IGNORECASE)
    return int(year_match.group(1)) if year_match else 9999

def extraer_titulo(entrada):
    """Extrae el título de una entrada .bib ('' si no existe)."""
    title_match = re.search(r'(?m)^\s*title\s*=\s*{(.+?)}', entrada, flags=re.DOTALL | re.IGNORECASE)
    return title_match.group(1).strip().lower() if title_match else ""

# -------------------------------
# Pigeonhole Sort (sin clave-valor)
# -------------------------------
def pigeonholeSort(arr):
    if not arr:
        return arr

    # Extraer el rango de años
    años = [extraer_year(e) for e in arr]
    min_year = min(años)
    max_year = max(años)
    rango = max_year - min_year + 1

    # Crear "agujeros" para cada año
    holes = [[] for _ in range(rango)]

    # Distribuir entradas en los agujeros correspondientes
    for entrada in arr:
        year = extraer_year(entrada)
        holes[year - min_year].append(entrada)

    # Reconstruir arreglo ordenado
    resultado = []
    for bucket in holes:
        # Dentro de cada bucket, ordenar por título
        bucket.sort(key=lambda e: extraer_titulo(e))
        resultado.extend(bucket)

    return resultado

# -------------------------------
# Parte principal para .bib
# -------------------------------
if __name__ == "__main__":
    # 1️⃣ Leer archivo original
    with open("articulos_con_titulo_y_abstract.bib", "r", encoding="utf-8") as f:
        contenido = f.read()

    # 2️⃣ Separar entradas
    entradas = re.split(r'(?=@\w+{)', contenido, flags=re.MULTILINE)
    entradas = [e.strip() for e in entradas if e.strip()]

    # 3️⃣ Ordenar con Pigeonhole Sort fiel
    start_time = time.perf_counter()
    entradas_ordenadas = pigeonholeSort(entradas)
    end_time = time.perf_counter()

    # 4️⃣ Guardar archivo ordenado
    with open("articulos_ordenados_pigeonholeSort.bib", "w", encoding="utf-8") as f:
        for e in entradas_ordenadas:
            f.write(e + "\n\n")

    # 5️⃣ Reporte
    print("✅ Ordenamiento completado con Pigeonhole Sort (fiel al algoritmo)")
    print(f"📚 Total entradas: {len(entradas_ordenadas)}")
    print(f"⏱ Tiempo: {end_time - start_time:.6f} segundos")
