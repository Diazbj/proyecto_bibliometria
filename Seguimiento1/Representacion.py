import re
import time
import matplotlib.pyplot as plt
from collections import Counter

from Seguimiento1.BitonicSort import bitonic_sort_rec, bitonic_sort_wrapper
from Seguimiento1.QuickSort import quicksort_wrapper
# -------------------------------
# Importar los 12 algoritmos
# -------------------------------
from TreeSort import tree_sort
from BinaryInsertionSort import binary_insertion_sort
from SelectionSort import selectionSort
from QuickSort import quick_sort
from HeapSort import heap_sort
from RadixSort import radix_sort
from GnomeSort import gnome_sort
from CombSort import comb_sort
from BucketSort import bucket_sort
from BitonicSort import bitonic_sort
from PigeonholeSort import pigeonholeSort
from TimSort import timSort

# -------------------------------
# Funciones auxiliares
# -------------------------------
def extraer_autores(entrada):
    """Extrae lista de autores de una entrada .bib"""
    match = re.search(r'author\s*=\s*{(.+?)}', entrada, flags=re.DOTALL | re.IGNORECASE)
    if not match:
        return []
    autores = match.group(1).replace("\n", " ").split(" and ")
    return [a.strip() for a in autores if a.strip()]

# -------------------------------
# Medición de tiempo
# -------------------------------
def medir_tiempo(func, arr):
    copia = arr[:]  # copiar para no afectar a otros algoritmos
    start = time.perf_counter()
    func(copia)     # cada algoritmo modifica la lista in-place
    end = time.perf_counter()
    return end - start

# -------------------------------
# Parte principal
# -------------------------------
if __name__ == "__main__":
    # 1️⃣ Leer archivo .bib
    with open("articulos_con_titulo_y_abstract.bib", "r", encoding="utf-8") as f:
        contenido = f.read()

    # 2️⃣ Separar entradas
    entradas = re.split(r'(?=@\w+{)', contenido, flags=re.MULTILINE)
    entradas = [e.strip() for e in entradas if e.strip()]

    # 3️⃣ Definir algoritmos a probar
    algoritmos = {
        "tree_sort": tree_sort,
        "binary_insert": binary_insertion_sort,
        "SelectionSort": selectionSort,
        "QuickSort": quicksort_wrapper,
        "HeapSort": heap_sort,
        "RadixSort": radix_sort,
        "GnomeSort": gnome_sort,
        "CombSort": comb_sort,
        "BucketSort": bucket_sort,
        "BitonicSort": bitonic_sort_wrapper,
        "PigeonholeSort": pigeonholeSort,
        "TimSort": timSort
    }

    # 4️⃣ Medir tiempos
    tiempos = {}
    for nombre, func in algoritmos.items():
        print(f"⏳ Ejecutando {nombre} ...")
        t = medir_tiempo(func, entradas)
        tiempos[nombre] = t
        print(f"   → {t:.6f} segundos")

    # 5️⃣ Graficar tiempos
    tiempos_ordenados = dict(sorted(tiempos.items(), key=lambda x: x[1]))
    plt.bar(tiempos_ordenados.keys(), tiempos_ordenados.values())
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Tiempo (segundos)")
    plt.title("Comparación de tiempos de algoritmos de ordenamiento")
    plt.tight_layout()
    plt.show()

    # 6️⃣ Top 15 autores
    autores = []
    for entrada in entradas:
        autores.extend(extraer_autores(entrada))

    contador = Counter(autores)
    top15 = contador.most_common(15)

    print("\n📊 Top 15 autores con más apariciones:")
    for autor, freq in top15:
        print(f"{autor}: {freq}")

    # 7️⃣ Gráfico de autores
    autores_labels = [autor for autor, _ in top15]
    frecuencias = [freq for _, freq in top15]

    plt.barh(autores_labels, frecuencias,color="limegreen")  # gráfico de barras horizontales
    plt.xlabel("Número de apariciones")
    plt.ylabel("Autores")
    plt.title("Top 15 autores con más apariciones en productos académicos")
    plt.gca().invert_yaxis()  # para que el autor más frecuente quede arriba
    plt.tight_layout()
    plt.show()
