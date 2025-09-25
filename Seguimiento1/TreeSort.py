import re
import time

# -------------------------------
# Algoritmo Tree Sort
# -------------------------------

class Node:
    """Nodo de un Árbol Binario de Búsqueda (BST)"""
    def __init__(self, key, value):
        self.key = key      # clave de ordenamiento (año, título)
        self.value = value  # entrada .bib original
        self.left = None
        self.right = None


def insert(root, key, value):
    """Inserta un nodo en el árbol BST"""
    if root is None:
        return Node(key, value)
    if key < root.key:
        root.left = insert(root.left, key, value)
    else:
        root.right = insert(root.right, key, value)
    return root


def inorder(root, result):
    """Recorrido in-order para recolectar entradas ordenadas"""
    if root is not None:
        inorder(root.left, result)
        result.append(root.value)
        inorder(root.right, result)


def tree_sort(arr):
    """Ordena usando Tree Sort con un BST"""
    root = None
    for key, value in arr:
        root = insert(root, key, value)
    result = []
    inorder(root, result)
    return result


# -------------------------------
# Funciones para trabajar con .bib
# -------------------------------

def extraer_datos(entrada):
    """Extrae (año, título) de una entrada .bib"""
    year_match = re.search(r'year\s*=\s*{(\d+)}', entrada, flags=re.IGNORECASE)
    # usamos ^ para evitar confundir title con booktitle
    title_match = re.search(r'(?m)^\s*title\s*=\s*{(.+?)}', entrada,
                            flags=re.DOTALL | re.IGNORECASE)

    year = int(year_match.group(1)) if year_match else 9999
    title = title_match.group(1).strip() if title_match else ""
    return year, title


# -------------------------------
# Parte principal
# -------------------------------
if __name__ == "__main__":
    # Leer archivo de entrada (.bib unificado)
    with open("articulos_con_titulo_y_abstract.bib", "r", encoding="utf-8") as f:
        contenido = f.read()

    # Separar entradas .bib
    entradas = re.split(r'(?=@\w+{)', contenido, flags=re.MULTILINE)
    entradas = [e.strip() for e in entradas if e.strip()]

    # Preprocesar claves una sola vez → [(clave, entrada)]
    entradas_con_clave = [(extraer_datos(e), e) for e in entradas]

    # Ordenar con Tree Sort
    start_time = time.perf_counter()
    entradas_ordenadas = tree_sort(entradas_con_clave)
    end_time = time.perf_counter()

    # Guardar archivo ordenado
    with open("articulos_ordenados_treeSort.bib", "w", encoding="utf-8") as f:
        for e in entradas_ordenadas:
            f.write(e + "\n\n")

    # Reporte
    print("Ordenamiento completado con Tree Sort")
    print(f"Total entradas: {len(entradas_ordenadas)}")
    print(f"Tiempo: {end_time - start_time:.6f} segundos")
