import bibtexparser
import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def cargar_articulos_bib(ruta_archivo):
    """
    Carga artículos desde un archivo .bib y extrae título y abstract.
    Devuelve una lista de diccionarios, donde cada diccionario representa un artículo.
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

def calcular_frecuencia_palabras_asociadas(abstracts, palabras_asociadas):
    """
    Calcula y presenta la frecuencia de aparición de un listado de palabras
    en una colección de abstracts.
    """
    texto_completo = " ".join(abstracts).lower()
    frecuencias = {}
    for palabra in palabras_asociadas:
        patron = r'\b' + re.escape(palabra.lower()) + r'\b'
        count = len(re.findall(patron, texto_completo))
        frecuencias[palabra] = count
    return frecuencias

def generar_nuevas_palabras_tfidf(abstracts, num_palabras=15):
    """
    Analiza todos los abstracts con TF-IDF y genera un listado de las palabras más relevantes.
    """
    print("\nAnalizando abstracts con TF-IDF para generar nuevas palabras clave...")
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_df=0.85, min_df=2)
    tfidf_matrix = vectorizer.fit_transform(abstracts)
    feature_names = np.array(vectorizer.get_feature_names_out())
    sum_tfidf = tfidf_matrix.sum(axis=0)
    scores = [(feature_names[col], sum_tfidf[0, col]) for col in range(tfidf_matrix.shape[1])]
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    mejores_terminos = [termino for termino, puntaje in sorted_scores[:num_palabras]]
    return mejores_terminos

if __name__ == "__main__":
    print("--- Requerimiento 3: Análisis de Frecuencia de Palabras Clave ---")
    
    categoria = "Concepts of Generative AI in Education"
    palabras_asociadas_originales = [
        "Generative models", "Prompting", "Machine learning", "Multimodality", 
        "Fine-tuning", "Training data", "Algorithmic bias", "Explainability", 
        "Transparency", "Ethics", "Privacy", "Personalization", 
        "Human-AI interaction", "AI literacy", "Co-creation"
    ]

    ruta_bib = 'archivos/articulos_con_titulo_y_abstract.bib'
    print(f"\nCargando artículos desde: {ruta_bib}")
    lista_articulos = cargar_articulos_bib(ruta_bib)
    
    if lista_articulos:
        print(f"Se cargaron {len(lista_articulos)} artículos.")
        
        corpus_abstracts = [articulo['abstract'] for articulo in lista_articulos]
        
        print(f"\nCalculando frecuencia para la categoría: '{categoria}'...")
        frecuencias = calcular_frecuencia_palabras_asociadas(corpus_abstracts, palabras_asociadas_originales)
        print("\n--- Frecuencia de Palabras Clave Predefinidas ---")
        for palabra, freq in sorted(frecuencias.items(), key=lambda item: item[1], reverse=True):
            print(f"- {palabra}: {freq} apariciones")

        nuevas_palabras = generar_nuevas_palabras_tfidf(corpus_abstracts, num_palabras=15)
        
        print("\n--- Nuevas Palabras Clave Generadas por TF-IDF (Top 15) ---")
        for palabra in nuevas_palabras:
            print(f"- {palabra}")
            
        print("\n--- Análisis de Precisión de las Nuevas Palabras ---")
        
        set_originales = {p.lower() for p in palabras_asociadas_originales}
        set_nuevas = {p.lower() for p in nuevas_palabras}
        
        palabras_comunes = set_originales.intersection(set_nuevas)
        
        if not nuevas_palabras:
            precision = 0.0
        else:
            precision = len(palabras_comunes) / len(nuevas_palabras)
            
        print(f"Palabras comunes encontradas: {len(palabras_comunes)}")
        if palabras_comunes:
            for palabra in palabras_comunes:
                print(f"  - {palabra}")
        
        print(f"\nPrecisión calculada: {precision:.2%} ({len(palabras_comunes)} de {len(nuevas_palabras)} palabras generadas estaban en la lista original).")
        print("Interpretación: Esta métrica de 'precisión' mide qué tan bien el algoritmo TF-IDF reproduce la lista de palabras clave original.")

    else:
        print("No se encontraron artículos en el archivo especificado.")
