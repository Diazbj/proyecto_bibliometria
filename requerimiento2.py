import bibtexparser
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import numpy as np

# --- Explicación del Algoritmo: Distancia de Levenshtein ---
# La Distancia de Levenshtein es una métrica de "distancia de edición" que mide cuán diferentes
# son dos cadenas de texto. El valor representa el número mínimo de ediciones de un solo
# carácter (inserciones, eliminaciones o sustituciones) necesarias para cambiar una cadena
# en la otra.
#
# Funcionamiento Algorítmico:
# 1. Crear una Matriz: Se construye una matriz de (longitud_texto1 + 1) x (longitud_texto2 + 1).
# 2. Inicializar la Matriz: La primera fila se inicializa con valores de 0 a longitud_texto1
#    y la primera columna con valores de 0 a longitud_texto2. Esto representa el costo de
#    convertir una cadena vacía en un prefijo de la otra.
# 3. Llenar la Matriz: Se itera a través de la matriz. Para cada celda (i, j), se calcula el
#    costo basándose en los caracteres texto1[i-1] y texto2[j-1]:
#    a) Si los caracteres son iguales, el costo es 0. Si son diferentes, el costo es 1.
#    b) El valor de la celda (i, j) se establece como el mínimo de las tres celdas vecinas
#       (izquierda, arriba, diagonal) más el costo correspondiente a la operación:
#       - Celda de arriba + 1 (corresponde a una eliminación).
#       - Celda de la izquierda + 1 (corresponde a una inserción).
#       - Celda diagonal + costo de sustitución (0 o 1).
# 4. Resultado Final: El valor en la esquina inferior derecha de la matriz es la distancia
#    de Levenshtein total entre las dos cadenas.

def calcular_distancia_levenshtein(texto1, texto2):
    """
    Calcula la distancia de Levenshtein entre dos textos.
    """
    size_x = len(texto1) + 1
    size_y = len(texto2) + 1
    matrix = np.zeros((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if texto1[x - 1] == texto2[y - 1]:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1],
                    matrix[x, y - 1] + 1
                )
            else:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1] + 1,
                    matrix[x, y - 1] + 1
                )
    return matrix[size_x - 1, size_y - 1]

# --- Explicación del Algoritmo: Similitud de Jaccard ---
# La similitud de Jaccard es una métrica estadística utilizada para medir la similitud y
# diversidad de conjuntos de muestras. Se define como el tamaño de la intersección dividido
# por el tamaño de la unión de los dos conjuntos.
#
# Funcionamiento Algorítmico:
# 1. Tokenización: Cada texto se divide en un conjunto de palabras (tokens). Se eliminan
#    las palabras duplicadas para formar un conjunto único para cada texto.
# 2. Intersección: Se encuentra el conjunto de palabras que aparecen en AMBOS textos.
# 3. Unión: Se encuentra el conjunto de palabras que aparecen en CUALQUIERA de los dos textos.
# 4. Cálculo: Se divide el número de palabras en la intersección por el número de palabras
#    en la unión. El resultado es un valor entre 0 (sin similitud) y 1 (conjuntos idénticos).
#    Fórmula: J(A, B) = |A ∩ B| / |A ∪ B|

def calcular_similitud_jaccard(texto1, texto2):
    """
    Calcula la similitud de Jaccard entre dos textos.
    """
    set1 = set(texto1.lower().split())
    set2 = set(texto2.lower().split())
    interseccion = set1.intersection(set2)
    union = set1.union(set2)
    return len(interseccion) / len(union)

# --- Explicación del Algoritmo: TF-IDF y Similitud del Coseno ---
# TF-IDF (Term Frequency-Inverse Document Frequency) es una técnica de vectorización que
# refleja la importancia de una palabra en un documento en relación con un corpus.
#
# Funcionamiento Algorítmico:
# 1. Cálculo de TF (Frecuencia de Término): Mide la frecuencia con la que aparece un término
#    en un documento. TF(t, d) = (Nº de veces que el término t aparece en el documento d).
# 2. Cálculo de IDF (Frecuencia Inversa de Documento): Mide la importancia de un término en
#    todo el corpus. Penaliza las palabras comunes (como "el", "es").
#    IDF(t, D) = log(Nº total de documentos / (1 + Nº de documentos con el término t)).
# 3. Ponderación TF-IDF: Se calcula multiplicando TF por IDF. Las palabras con una alta
#    puntuación TF-IDF son frecuentes en un documento pero raras en el resto del corpus,
#    lo que las hace buenas para caracterizar el documento.
# 4. Vectorización: Cada documento se convierte en un vector numérico donde cada componente
#    es la puntuación TF-IDF de una palabra del vocabulario.
# 5. Similitud del Coseno: Se calcula el coseno del ángulo entre los dos vectores de
#    documento. Un valor cercano a 1 significa que los vectores apuntan en una dirección
#    similar (alta similitud), mientras que un valor cercano a 0 indica baja similitud.

def calcular_similitud_tfidf_coseno(texto1, texto2, corpus):
    """
    Calcula la similitud del coseno entre dos textos usando vectores TF-IDF.
    """
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(corpus)
    # Encontrar los índices de los textos en el corpus para obtener sus vectores
    idx1 = corpus.index(texto1)
    idx2 = corpus.index(texto2)
    vector1 = tfidf_matrix[idx1]
    vector2 = tfidf_matrix[idx2]
    return cosine_similarity(vector1, vector2)[0][0]

# --- Explicación del Algoritmo: Bag of Words (BoW) y Similitud del Coseno ---
# Bag of Words es un modelo de representación de texto que lo describe a través de la
# frecuencia de sus palabras, ignorando el orden y la gramática.
#
# Funcionamiento Algorítmico:
# 1. Tokenización: Se divide el texto en palabras (tokens).
# 2. Construcción de Vocabulario: Se crea un vocabulario con todas las palabras únicas
#    presentes en el corpus.
# 3. Vectorización: Para cada documento, se crea un vector del tamaño del vocabulario.
#    Cada componente del vector corresponde a una palabra del vocabulario y su valor es
#    el número de veces que esa palabra aparece en el documento.
# 4. Similitud del Coseno: Al igual que con TF-IDF, se calcula la similitud del coseno
#    entre los vectores BoW de los dos documentos para medir su similitud.

def calcular_similitud_bow_coseno(texto1, texto2):
    """
    Calcula la similitud del coseno entre dos textos usando vectores Bag of Words.
    """
    vectorizer = CountVectorizer(stop_words='english')
    bow_matrix = vectorizer.fit_transform([texto1, texto2])
    return cosine_similarity(bow_matrix[0:1], bow_matrix[1:2])[0][0]

# --- Explicación del Algoritmo: Sentence-BERT (SBERT) (IA) ---
# SBERT es un modelo de red neuronal pre-entrenado (basado en la arquitectura Transformer)
# que está especializado en crear "embeddings" (vectores) de alta calidad para frases y
# párrafos completos, capturando su significado semántico contextual.
#
# Funcionamiento Algorítmico:
# 1. Modelo Pre-entrenado: Se carga un modelo SBERT que ya ha sido entrenado en una enorme
#    cantidad de texto para entender las relaciones semánticas entre palabras y frases.
# 2. Inferencia de Vectores (Embeddings): Cada texto (abstract) se pasa a través del modelo
#    SBERT. El modelo procesa el texto y genera un vector de tamaño fijo (por ejemplo, 384
#    dimensiones para 'all-MiniLM-L6-v2') que representa el significado del texto completo.
#    A diferencia de BoW o TF-IDF, SBERT entiende el contexto ("banco" de sentarse vs.
#    "banco" de dinero).
# 3. Similitud del Coseno: Se calcula la similitud del coseno entre los dos vectores
#    generados. Un valor alto indica que los dos textos son semánticamente muy similares,
#    incluso si no usan exactamente las mismas palabras.

def calcular_similitud_sbert(texto1, texto2, model):
    """
    Calcula la similitud semántica entre dos textos usando Sentence-BERT.
    """
    embeddings = model.encode([texto1, texto2], convert_to_tensor=True)
    similitud = util.cos_sim(embeddings[0], embeddings[1])
    return similitud.item()

# --- Explicación del Algoritmo: Doc2Vec (IA) ---
# Doc2Vec es una extensión del algoritmo Word2Vec y su objetivo es crear una representación
# vectorial de un documento completo (como un párrafo o un artículo), no solo de palabras
# individuales. Estos vectores, al igual que en SBERT, capturan el significado semántico.
#
# Funcionamiento Algorítmico:
# 1. Preprocesamiento y Etiquetado: Cada documento del corpus se tokeniza (divide en palabras)
#    y se le asigna una etiqueta única.
# 2. Construcción de Vocabulario y Entrenamiento: El modelo Doc2Vec se entrena sobre el corpus
#    etiquetado. Aprende simultáneamente vectores para las palabras y para las etiquetas de
#    los documentos, intentando predecir palabras en un contexto. El vector del documento
#    aprende a representar el tema o contexto general del texto.
# 3. Inferencia de Vectores: Para comparar dos documentos, el modelo "infiere" un nuevo vector
#    para cada uno, basándose en el conocimiento que ya tiene del corpus.
# 4. Cálculo de Similitud: Se calcula la similitud del coseno entre los dos vectores inferidos.

def calcular_similitud_doc2vec(texto1, texto2, corpus):
    """
    Calcula la similitud semántica entre dos textos usando un modelo Doc2Vec entrenado.
    """
    documentos_etiquetados = [TaggedDocument(words=gensim.utils.simple_preprocess(doc), tags=[i]) for i, doc in enumerate(corpus)]
    print("Entrenando modelo Doc2Vec (esto puede tardar)...")
    model = Doc2Vec(vector_size=50, window=5, min_count=2, workers=4, epochs=40)
    model.build_vocab(documentos_etiquetados)
    model.train(documentos_etiquetados, total_examples=model.corpus_count, epochs=model.epochs)
    print("Modelo Doc2Vec entrenado.")
    vector1 = model.infer_vector(gensim.utils.simple_preprocess(texto1))
    vector2 = model.infer_vector(gensim.utils.simple_preprocess(texto2))
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
        if 'title' in entry and 'abstract' in entry:
            articulos.append({
                'id': entry.get('ID', 'N/A'),
                'title': entry['title'],
                'abstract': entry['abstract']
            })
    return articulos

def seleccionar_articulo(lista_articulos, mensaje):
    """
    Muestra una lista de artículos y pide al usuario que seleccione uno por su índice.
    """
    print("\n--- Lista de Artículos Disponibles ---")
    for i, articulo in enumerate(lista_articulos):
        print(f"[{i}] {articulo['title']}")
    
    while True:
        try:
            idx = int(input(f"\n{mensaje} (ingrese el número): "))
            if 0 <= idx < len(lista_articulos):
                return lista_articulos[idx]
            else:
                print(f"Error: Por favor, ingrese un número entre 0 y {len(lista_articulos) - 1}.")
        except ValueError:
            print("Error: Por favor, ingrese un número válido.")

if __name__ == "__main__":
    ruta_bib = 'archivos/articulos_con_titulo_y_abstract.bib'
    print(f"Cargando artículos desde: {ruta_bib}")
    lista_articulos = cargar_articulos_bib(ruta_bib)

    if len(lista_articulos) >= 2:
        print(f"Se cargaron {len(lista_articulos)} artículos con título y abstract.")

        # --- Selección de Artículos (Modificado para no ser interactivo) ---
        # Se seleccionan los dos primeros artículos de la lista por defecto.
        print("Seleccionando los dos primeros artículos de la lista para la comparación automática.")
        articulo1 = lista_articulos[0]
        articulo2 = lista_articulos[1]

        print(f"\n--- Artículos Seleccionados para Comparación ---")
        print(f"Artículo 1: {articulo1['title']}")
        print(f"Artículo 2: {articulo2['title']}")

        corpus_abstracts = [articulo['abstract'] for articulo in lista_articulos]
        
        # --- 1. Comparación con Distancia de Levenshtein ---
        print("\n--- Algoritmo 1: Distancia de Levenshtein ---")
        # Se usa en una porción para que sea computacionalmente manejable
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