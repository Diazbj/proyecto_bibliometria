import re
import time

# -------------------------------
# Nodo de Árbol Binario (BST)
# -------------------------------
class Node:
    """Nodo de un Árbol Binario de Búsqueda (BST)"""
    def __init__(self, value):
        self.value = value  # entrada .bib original
        self.left = None
        self.right = None

# -------------------------------
# Funciones auxiliares de extracción
# -------------------------------
def extraer_year(entrada):
    match = re.search(r'year\s*=\s*[{"](\d+)[}"]', entrada, flags=re.IGNORECASE)
    return int(match.group(1)) if match else 9999

def extraer_title(entrada):
    match = re.search(r'(?m)^\s*title\s*=\s*[{"](.+?)[}"]', entrada, flags=re.DOTALL | re.IGNORECASE)
    return match.group(1).strip().lower() if match else ""

# -------------------------------
# Comparador de entradas por año y título
# -------------------------------
def es_menor(e1, e2):
    year1, title1 = extraer_year(e1), extraer_title(e1)
    year2, title2 = extraer_year(e2), extraer_title(e2)

    # Primero por año, luego por título
    if year1 < year2:
        return True
    if year1 == year2 and title1 < title2:
        return True
    return False

# -------------------------------
# Inserción en el árbol BST (fiel)
# -------------------------------
def insert(root, value):
    if root is None:
        return Node(value)

    if es_menor(value, root.value):
        root.left = insert(root.left, value)
    else:
        root.right = insert(root.right, value)
    return root

# -------------------------------
# Recorrido in-order (recolecta en orden ascendente)
# -------------------------------
def inorder(root, result):
    if root is not None:
        inorder(root.left, result)
        result.append(root.value)
        inorder(root.right, result)

# -------------------------------
# Algoritmo Tree Sort original
# -------------------------------
def tree_sort(arr):
    root = None
    for item in arr:
        root = insert(root, item)
    result = []
    inorder(root, result)
    return result

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

    # Ordenar con Tree Sort fiel
    start_time = time.perf_counter()
    entradas_ordenadas = tree_sort(entradas)
    end_time = time.perf_counter()

    # Guardar archivo ordenado
    with open("articulos_ordenados_treeSort.bib", "w", encoding="utf-8") as f:
        for e in entradas_ordenadas:
            f.write(e + "\n\n")

    # Reporte
    print("✅ Ordenamiento completado con Tree Sort (fiel, sin clave)")
    print(f"📄 Total entradas: {len(entradas_ordenadas)}")
    print(f"⏱️ Tiempo: {end_time - start_time:.6f} segundos")
