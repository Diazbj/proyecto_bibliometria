import bibtexparser
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

# --- Explicación del Algoritmo: Distancia de Levenshtein ---
# (Explicación sin cambios...)

def calcular_distancia_levenshtein(texto1, texto2):
    """
    Calcula la distancia de Levenshtein entre dos textos.
    """
    # (Código sin cambios...)

# --- Explicación del Algoritmo: Similitud de Jaccard ---
# (Explicación sin cambios...)

def calcular_similitud_jaccard(texto1, texto2):
    """
    Calcula la similitud de Jaccard entre dos textos.
    """
    # (Código sin cambios...)

# --- Explicación del Algoritmo: TF-IDF y Similitud del Coseno ---
# (Explicación sin cambios...)

def calcular_similitud_tfidf_coseno(texto1, texto2, corpus):
    """
    Calcula la similitud del coseno entre dos textos usando vectores TF-IDF.
    """
    # (Código sin cambios...)

# --- Explicación del Algoritmo: Bag of Words (BoW) y Similitud del Coseno ---
# (Explicación sin cambios...)

def calcular_similitud_bow_coseno(texto1, texto2):
    """
    Calcula la similitud del coseno entre dos textos usando vectores Bag of Words.
    """
    # (Código sin cambios...)

# --- Explicación del Algoritmo: Sentence-BERT (SBERT) ---
# (Explicación sin cambios...)

def calcular_similitud_sbert(texto1, texto2, model):
    """
    Calcula la similitud semántica entre dos textos usando Sentence-BERT.
    """
    # (Código sin cambios...)

# --- Explicación del Algoritmo: Doc2Vec (IA) ---
# Doc2Vec es una extensión del algoritmo Word2Vec y su objetivo es crear una representación
# vectorial de un documento completo (como un párrafo o un artículo), no solo de palabras
# individuales. Estos vectores, al igual que en SBERT, capturan el significado semántico.
#
# Funcionamiento Algorítmico:
# 1. Preprocesamiento y Etiquetado: Cada documento del corpus se tokeniza (divide en palabras)
#    y se le asigna una etiqueta única. El formato resultante es una lista de objetos
#    `TaggedDocument`, donde cada uno contiene los tokens y su etiqueta.
# 2. Construcción de Vocabulario: El modelo Doc2Vec analiza todo el corpus para construir un
#    vocabulario de todas las palabras presentes.
# 3. Entrenamiento del Modelo: El modelo se entrena sobre el corpus etiquetado. Durante este
#    proceso, aprende dos cosas simultáneamente:
#    a) Vectores para las palabras (como en Word2Vec).
#    b) Vectores para las etiquetas de los documentos.
#    El modelo intenta predecir palabras en un contexto, utilizando tanto los vectores de
#    palabras cercanas como el vector del documento completo. Así, el vector del documento
#    aprende a representar el tema o contexto general del texto.
# 4. Inferencia de Vectores: Para comparar dos documentos, incluso si no estaban en el corpus
#    de entrenamiento, el modelo puede "inferir" un nuevo vector para cada uno, basándose en
#    el conocimiento que ya tiene.
# 5. Cálculo de Similitud: Se calcula la similitud del coseno entre los dos vectores inferidos.

def calcular_similitud_doc2vec(texto1, texto2, corpus):
    """
    Calcula la similitud semántica entre dos textos usando un modelo Doc2Vec entrenado.
    """
    # Preprocesar y etiquetar todo el corpus
    documentos_etiquetados = [TaggedDocument(words=gensim.utils.simple_preprocess(doc), tags=[i]) for i, doc in enumerate(corpus)]

    # Inicializar y entrenar el modelo Doc2Vec
    # vector_size: dimensionalidad de los vectores; window: tamaño de la ventana de contexto;
    # min_count: ignora palabras con frecuencia menor a esta; workers: hilos de CPU a usar.
    print("Entrenando modelo Doc2Vec (esto puede tardar)...")
    model = Doc2Vec(vector_size=50, window=5, min_count=2, workers=4, epochs=20)
    model.build_vocab(documentos_etiquetados)
    model.train(documentos_etiquetados, total_examples=model.corpus_count, epochs=model.epochs)
    print("Modelo Doc2Vec entrenado.")

    # Inferir vectores para los dos textos de interés
    vector1 = model.infer_vector(gensim.utils.simple_preprocess(texto1))
    vector2 = model.infer_vector(gensim.utils.simple_preprocess(texto2))

    # Calcular similitud del coseno (reshape es necesario para la función de sklearn)
    similitud = cosine_similarity(vector1.reshape(1, -1), vector2.reshape(1, -1))
    return similitud[0][0]

def cargar_articulos_bib(ruta_archivo):
    """
    Carga artículos desde un archivo .bib y extrae título y abstract.
    """
    with open(ruta_archivo, 'r', encoding='utf-8') as bibfile:
        bib_database = bibtexparser.load(bibfile)

    articulos = []
    for entry in bib_database.entries:
        # Asegurarse de que el artículo tenga tanto título como abstract
        if 'title' in entry and 'abstract' in entry:
            articulos.append({
                'id': entry.get('ID', 'N/A'),
                'title': entry['title'],
                'abstract': entry['abstract']
            })
    return articulos

if __name__ == "__main__":
    # Ruta al archivo BibTeX
    ruta_bib = 'archivos/articulos_con_titulo_y_abstract.bib'

    print(f"Cargando artículos desde: {ruta_bib}")
    lista_articulos = cargar_articulos_bib(ruta_bib)

    if len(lista_articulos) >= 2:
        print(f"Se cargaron {len(lista_articulos)} artículos con título y abstract.")

        # Crear un corpus con todos los abstracts para el cálculo de IDF y Doc2Vec
        corpus_abstracts = [articulo['abstract'] for articulo in lista_articulos]

        # Seleccionar dos artículos para comparar (por ejemplo, los dos primeros)
        articulo1 = lista_articulos[0]
        articulo2 = lista_articulos[1]

        print(f"\n--- Artículos de Muestra para Comparación ---")
        print(f"Artículo 1: {articulo1['title']}")
        print(f"Artículo 2: {articulo2['title']}")

        # --- 1. Comparación con Distancia de Levenshtein ---
        print("\n--- Algoritmo 1: Distancia de Levenshtein ---")
        abstract1_corto = articulo1['abstract'][:500]
        abstract2_corto = articulo2['abstract'][:500]
        distancia_lev = calcular_distancia_levenshtein(abstract1_corto, abstract2_corto)
        print(f"Distancia (primeros 500 caracteres): {distancia_lev}")
        print("Interpretación: Un valor más bajo indica mayor similitud (menos ediciones).")

        # --- 2. Comparación con Similitud de Jaccard ---
        print("\n--- Algoritmo 2: Similitud de Jaccard ---")
        similitud_jac = calcular_similitud_jaccard(articulo1['abstract'], articulo2['abstract'])
        print(f"Similitud: {similitud_jac:.4f}")
        print("Interpretación: Un valor cercano a 1.0 indica alta similitud (mucho vocabulario compartido).")

        # --- 3. Comparación con TF-IDF y Similitud del Coseno ---
        print("\n--- Algoritmo 3: TF-IDF + Similitud del Coseno ---")
        similitud_tfidf = calcular_similitud_tfidf_coseno(articulo1['abstract'], articulo2['abstract'], corpus_abstracts)
        print(f"Similitud: {similitud_tfidf:.4f}")
        print("Interpretación: Un valor cercano a 1.0 indica alta similitud semántica basada en palabras clave ponderadas.")

        # --- 4. Comparación con Bag of Words (BoW) y Similitud del Coseno ---
        print("\n--- Algoritmo 4: Bag of Words (BoW) + Similitud del Coseno ---")
        similitud_bow = calcular_similitud_bow_coseno(articulo1['abstract'], articulo2['abstract'])
        print(f"Similitud: {similitud_bow:.4f}")
        print("Interpretación: Un valor cercano a 1.0 indica alta similitud basada en la frecuencia de palabras compartidas.")

        # --- 5. Comparación con Sentence-BERT (IA) ---
        print("\n--- Algoritmo 5: Sentence-BERT (SBERT) + Similitud del Coseno ---")
        print("Cargando modelo SBERT (puede tardar y descargar datos la primera vez)...")
        sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Modelo SBERT cargado.")
        similitud_sbert = calcular_similitud_sbert(articulo1['abstract'], articulo2['abstract'], sbert_model)
        print(f"Similitud: {similitud_sbert:.4f}")
        print("Interpretación: Un valor cercano a 1.0 indica una alta similitud semántica contextual.")

        # --- 6. Comparación con Doc2Vec (IA) ---
        print("\n--- Algoritmo 6: Doc2Vec + Similitud del Coseno ---")
        similitud_d2v = calcular_similitud_doc2vec(articulo1['abstract'], articulo2['abstract'], corpus_abstracts)
        print(f"Similitud: {similitud_d2v:.4f}")
        print("Interpretación: Un valor cercano a 1.0 indica alta similitud basada en el contexto del documento aprendido del corpus.")

    else:
        print("No se encontraron suficientes artículos (se necesitan al menos 2) para realizar la comparación.")
