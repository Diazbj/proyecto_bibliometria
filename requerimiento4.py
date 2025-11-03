import bibtexparser
from sentence_transformers import SentenceTransformer
import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
import warnings

# Ignorar advertencias de Matplotlib sobre fuentes
warnings.filterwarnings("ignore", category=UserWarning, module='matplotlib')

def cargar_articulos_bib(ruta_archivo):
    """
    Carga artículos desde un archivo .bib y extrae título y abstract.
    """
    with open(ruta_archivo, 'r', encoding='utf-8') as bibfile:
        bib_database = bibtexparser.load(bibfile)
    articulos = []
    for entry in bib_database.entries:
        if 'title' in entry and 'abstract' in entry:
            articulos.append({
                'title': entry['title'].strip(),
                'abstract': entry['abstract']
            })
    return articulos

def realizar_clustering_y_graficar(embeddings, labels, method, file_name):
    """
    Realiza clustering jerárquico usando un método específico y guarda el dendrograma.
    """
    print(f"\nEjecutando clustering con el método: '{method}'...")

    metric_to_use = 'euclidean' if method == 'ward' else 'cosine'
    print(f"Usando la métrica de distancia: '{metric_to_use}'")

    # Realizar el clustering jerárquico
    linked = linkage(embeddings, method=method, metric=metric_to_use)
    
    # Configurar y generar el dendrograma
    plt.figure(figsize=(15, 8))
    dendrogram(
        linked,
        orientation='top',
        labels=labels,
        distance_sort='descending',
        show_leaf_counts=True,
        leaf_rotation=90.,  # Rotar las etiquetas para que sean legibles
        leaf_font_size=8.,
    )
    
    plt.title(f'Dendrograma de Clustering Jerárquico (Método: {method.capitalize()})')
    plt.ylabel("Distancia")
    plt.xlabel("Artículos")
    plt.tight_layout()  # Ajustar el layout para que no se corten las etiquetas
    
    # Guardar la figura
    try:
        plt.savefig(file_name, dpi=300)
        print(f"Dendrograma guardado en: {file_name}")
    except Exception as e:
        print(f"Error al guardar el archivo {file_name}: {e}")
    
    plt.close() # Cerrar la figura para liberar memoria

if __name__ == "__main__":
    print("--- Requerimiento 4: Clustering Jerárquico y Dendrogramas ---")

    # --- 1. Carga y Preprocesamiento de Datos ---
    ruta_bib = 'archivos/articulos_con_titulo_y_abstract.bib'
    print(f"\nCargando artículos desde: {ruta_bib}")
    lista_articulos = cargar_articulos_bib(ruta_bib)
    
    if len(lista_articulos) > 1:
        # Para demostración, usar un subconjunto de artículos para que el dendrograma sea legible
        num_articulos_demo = 25
        if len(lista_articulos) > num_articulos_demo:
            print(f"Se usarán los primeros {num_articulos_demo} artículos para la demostración.")
            lista_articulos = lista_articulos[:num_articulos_demo]
        
        corpus_abstracts = [articulo['abstract'] for articulo in lista_articulos]
        # Truncar títulos largos para que quepan en el gráfico
        labels = [f"{(articulo['title'][:75] + '...') if len(articulo['title']) > 75 else articulo['title']}" for articulo in lista_articulos]

        # --- 2. Transformación de Texto a Vectores (Embeddings) ---
        print("\nCargando modelo Sentence-BERT para vectorizar los abstracts...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Generando embeddings... (esto puede tardar)")
        embeddings = model.encode(corpus_abstracts, show_progress_bar=True)
        
        # --- 3. Aplicación de Algoritmos y Visualización ---
        metodos_clustering = ['ward', 'complete', 'average']
        
        for metodo in metodos_clustering:
            nombre_archivo = "dendrograma_{}.png".format(metodo)
            realizar_clustering_y_graficar(embeddings, labels, metodo, nombre_archivo)
            
        print("\nAnálisis de coherencia:")
        print("- Ward: Generalmente produce clusters bien balanceados y es un buen punto de partida.")
        print("- Complete Linkage: Tiende a encontrar clusters compactos. Es sensible a outliers.")
        print("- Average Linkage: Menos sensible a outliers que Complete Linkage. Un buen compromiso.")
        print("\nPara determinar cuál es 'más coherente', se deben inspeccionar visualmente los dendrogramas y ver qué agrupación parece tener más sentido temático.")

    else:
        print("No se encontraron suficientes artículos para realizar el clustering.")