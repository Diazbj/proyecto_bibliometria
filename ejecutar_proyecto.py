# -*- coding: utf-8 -*-
import os
import bibtexparser
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import plotly.express as px
import pycountry_convert as pc
import re
from fpdf import FPDF
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from scipy.cluster.hierarchy import linkage, dendrogram
import warnings

# --- Funciones del Requerimiento 1 ---
def concat_bib_files(folders, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as outfile:
        for folder in folders:
            for filename in os.listdir(folder):
                if filename.endswith(".bib"):
                    filepath = os.path.join(folder, filename)
                    with open(filepath, "r", encoding="utf-8") as infile:
                        outfile.write(infile.read() + "\n")
    print(f"Archivos de {folders} concatenados en {output_file}")

def remove_duplicates(input_file, output_unique, output_duplicates, key="title"):
    with open(input_file, encoding="utf-8") as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    seen = set()
    unique_entries, duplicate_entries = [], []
    for entry in bib_database.entries:
        value = entry.get(key, "").strip().lower()
        if value:
            if value not in seen:
                seen.add(value)
                unique_entries.append(entry)
            else:
                duplicate_entries.append(entry)
    db_unique = bibtexparser.bibdatabase.BibDatabase()
    db_unique.entries = unique_entries
    writer = bibtexparser.bwriter.BibTexWriter()
    with open(output_unique, "w", encoding="utf-8") as f:
        f.write(writer.write(db_unique))
    if duplicate_entries:
        db_duplicates = bibtexparser.bibdatabase.BibDatabase()
        db_duplicates.entries = duplicate_entries
        with open(output_duplicates, "w", encoding="utf-8") as f:
            f.write(writer.write(db_duplicates))
    print(f"{len(unique_entries)} artículos únicos guardados en {output_unique}")
    print(f"{len(duplicate_entries)} duplicados guardados en {output_duplicates}")

# --- Funciones de Verificación (Parte del Req 1) ---
def verificar_y_filtrar(input_file, output_validos, output_eliminados):
    with open(input_file, encoding="utf-8") as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    validos, eliminados = [], []
    for entry in bib_database.entries:
        if entry.get("title", "").strip() and entry.get("abstract", "").strip():
            validos.append(entry)
        else:
            eliminados.append(entry)
    db_validos = bibtexparser.bibdatabase.BibDatabase()
    db_validos.entries = validos
    writer = bibtexparser.bwriter.BibTexWriter()
    with open(output_validos, "w", encoding="utf-8") as f:
        f.write(writer.write(db_validos))
    if eliminados:
        db_eliminados = bibtexparser.bibdatabase.BibDatabase()
        db_eliminados.entries = eliminados
        with open(output_eliminados, "w", encoding="utf-8") as f:
            f.write(writer.write(db_eliminados))
    print(f"Total de artículos: {len(bib_database.entries)}")
    print(f"Artículos válidos: {len(validos)} → guardados en {output_validos}")
    print(f"Artículos eliminados: {len(eliminados)} → guardados en {output_eliminados}")

# --- Funciones del Requerimiento 2 ---
def calcular_distancia_levenshtein(t1, t2):
    s_x, s_y = len(t1) + 1, len(t2) + 1
    matrix = np.zeros((s_x, s_y))
    for x in range(s_x): matrix[x, 0] = x
    for y in range(s_y): matrix[0, y] = y
    for x in range(1, s_x):
        for y in range(1, s_y):
            cost = 0 if t1[x - 1] == t2[y - 1] else 1
            matrix[x, y] = min(matrix[x-1, y] + 1, matrix[x, y-1] + 1, matrix[x-1, y-1] + cost)
    return matrix[s_x - 1, s_y - 1]

def calcular_similitud_jaccard(t1, t2):
    set1, set2 = set(t1.lower().split()), set(t2.lower().split())
    return len(set1.intersection(set2)) / len(set1.union(set2))

def calcular_similitud_tfidf_coseno(t1, t2, corpus):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(corpus)
    idx1, idx2 = corpus.index(t1), corpus.index(t2)
    return cosine_similarity(tfidf_matrix[idx1], tfidf_matrix[idx2])[0][0]

def calcular_similitud_bow_coseno(t1, t2):
    vectorizer = CountVectorizer(stop_words='english')
    bow_matrix = vectorizer.fit_transform([t1, t2])
    return cosine_similarity(bow_matrix[0:1], bow_matrix[1:2])[0][0]

def calcular_similitud_sbert(t1, t2, model):
    embeddings = model.encode([t1, t2], convert_to_tensor=True)
    return util.cos_sim(embeddings[0], embeddings[1]).item()

def calcular_similitud_doc2vec(t1, t2, corpus):
    docs = [TaggedDocument(words=gensim.utils.simple_preprocess(doc), tags=[i]) for i, doc in enumerate(corpus)]
    model = Doc2Vec(vector_size=50, window=5, min_count=2, workers=4, epochs=40)
    model.build_vocab(docs)
    model.train(docs, total_examples=model.corpus_count, epochs=model.epochs)
    v1 = model.infer_vector(gensim.utils.simple_preprocess(t1))
    v2 = model.infer_vector(gensim.utils.simple_preprocess(t2))
    return cosine_similarity(v1.reshape(1, -1), v2.reshape(1, -1))[0][0]

# --- Funciones del Requerimiento 3 ---
def calcular_frecuencia_palabras_asociadas(abstracts, palabras):
    texto_completo = " ".join(abstracts).lower()
    frecuencias = {p: len(re.findall(r'\b' + re.escape(p.lower()) + r'\b', texto_completo)) for p in palabras}
    return frecuencias

def generar_nuevas_palabras_tfidf(abstracts, num_palabras=15):
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_df=0.85, min_df=2)
    tfidf_matrix = vectorizer.fit_transform(abstracts)
    features = np.array(vectorizer.get_feature_names_out())
    sum_tfidf = tfidf_matrix.sum(axis=0)
    scores = sorted([(features[col], sum_tfidf[0, col]) for col in range(tfidf_matrix.shape[1])], key=lambda x: x[1], reverse=True)
    return [termino for termino, _ in scores[:num_palabras]]

# --- Funciones del Requerimiento 4 ---
def realizar_clustering_y_graficar(embeddings, labels, method, file_name):
    print(f"\nEjecutando clustering con el método: '{method}'...")
    metric = 'euclidean' if method == 'ward' else 'cosine'
    linked = linkage(embeddings, method=method, metric=metric)
    plt.figure(figsize=(15, 8))
    dendrogram(linked, orientation='top', labels=labels, distance_sort='descending', show_leaf_counts=True, leaf_rotation=90., leaf_font_size=8.)
    plt.title(f'Dendrograma de Clustering Jerárquico (Método: {method.capitalize()})')
    plt.ylabel("Distancia")
    plt.xlabel("Artículos")
    plt.tight_layout()
    plt.savefig(file_name, dpi=300)
    print(f"Dendrograma guardado en: {file_name}")
    plt.close()

# --- Funciones del Requerimiento 5 ---
def generar_nube_de_palabras(df, file_name):
    print("\n--- Generando Nube de Palabras ---")
    text = ' '.join(df['abstract'].fillna('')) + ' ' + ' '.join(df['keywords'].fillna(''))
    if not text.strip(): return
    stopwords = set(STOPWORDS)
    stopwords.update(["research", "paper", "study", "results", "model", "data", "analysis"])
    wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=stopwords, colormap='viridis').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(file_name, dpi=300)
    print(f"Nube de palabras guardada en: {file_name}")
    plt.close()

def generar_lineas_tiempo(df):
    print("\n--- Generando Gráficos de Líneas de Tiempo ---")
    if 'year' in df.columns:
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        pub_por_ano = df['year'].value_counts().sort_index()
        plt.figure(figsize=(10, 6))
        pub_por_ano.plot(kind='bar', color='skyblue')
        plt.title('Número de Publicaciones por Año')
        plt.xlabel('Año'); plt.ylabel('Número de Publicaciones')
        plt.xticks(rotation=45); plt.grid(axis='y', linestyle='--'); plt.tight_layout()
        plt.savefig("linea_temporal_año.png", dpi=300)
        print("Gráfico de publicaciones por año guardado.")
        plt.close()
    df['venue'] = df['journal'].fillna(df['booktitle'])
    if not df['venue'].dropna().empty:
        pub_por_venue = df['venue'].value_counts().nlargest(10)
        plt.figure(figsize=(10, 8))
        pub_por_venue.sort_values().plot(kind='barh', color='lightcoral')
        plt.title('Top 10 Revistas/Conferencias')
        plt.xlabel('Número de Publicaciones'); plt.ylabel('Revista o Conferencia')
        plt.tight_layout()
        plt.savefig("publicaciones_por_revista.png", dpi=300)
        print("Gráfico de publicaciones por revista guardado.")
        plt.close()

def generar_mapa_calor(df, file_name):
    print("\n--- Generando Mapa de Calor Geográfico ---")
    if 'author' not in df.columns: return
    country_map = {"USA": "United States", "UK": "United Kingdom", "UAE": "United Arab Emirates"}
    def get_country(aff):
        if not isinstance(aff, str): return None
        country = aff.split(',')[-1].strip()
        country = country_map.get(country, country)
        try: return pc.country_name_to_country_alpha3(country)
        except: return None
    df['iso_alpha'] = df['author'].apply(get_country)
    country_counts = df.dropna(subset=['iso_alpha'])['iso_alpha'].value_counts().reset_index()
    country_counts.columns = ['iso_alpha', 'publications']
    country_counts['country'] = country_counts['iso_alpha'].apply(lambda x: pc.country_alpha3_to_country_name(x))
    if country_counts.empty: return
    fig = px.choropleth(country_counts, locations="iso_alpha", color="publications", hover_name="country", color_continuous_scale=px.colors.sequential.Plasma, title="Distribución Geográfica de Publicaciones")
    fig.write_html(file_name)
    print(f"Mapa de calor guardado en: {file_name}")

def exportar_a_pdf(file_name):
    print("\n--- Exportando reporte a PDF ---")
    pdf = FPDF()
    images = {"nube_de_palabras.png": "1. Nube de Palabras Clave", "linea_temporal_año.png": "2.a. Publicaciones por Año", "publicaciones_por_revista.png": "2.b. Top 10 Revistas/Conferencias"}
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Reporte de Análisis Bibliométrico', 0, 1, 'C')
    pdf.ln(10)
    for img, title in images.items():
        if os.path.exists(img):
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, title, 0, 1)
            pdf.image(img, x=10, w=190)
            pdf.ln(5)
    if os.path.exists("mapa_calor_autores.html"):
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, '3. Distribución Geográfica (HTML Interactivo)', 0, 1)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(0, 10, 'El mapa de calor es interactivo. Abra el archivo "mapa_calor_autores.html" en un navegador.')
    pdf.output(file_name)
    print(f"Reporte PDF guardado en: {file_name}")

# --- Función para cargar artículos (usada por varios requerimientos) ---
def cargar_articulos_bib_reqs(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as bibfile:
        bib_database = bibtexparser.load(bibfile)
    articulos = []
    for entry in bib_database.entries:
        if 'title' in entry and 'abstract' in entry:
            articulos.append({'title': entry['title'], 'abstract': entry['abstract']})
    return articulos

# --- Main Execution Block ---
def main():
    print("--- INICIANDO EJECUCIÓN COMPLETA DEL PROYECTO ---")
    
    # --- REQUERIMIENTO 1: Limpieza y unificación de datos ---
    print("\n--- Ejecutando Requerimiento 1 ---")
    acm_folder = "archivos/descargaACM"
    sd_folder = "archivos/descargaScienceDirect"
    all_raw = "archivos/todos_raw.bib"
    final_clean = "archivos/articulos_unicos.bib"
    duplicates_file = "archivos/duplicados.bib"
    archivo_validos = "archivos/articulos_con_titulo_y_abstract.bib"
    archivo_eliminados = "archivos/articulos_eliminados.bib"
    
    concat_bib_files([acm_folder, sd_folder], all_raw)
    remove_duplicates(all_raw, final_clean, duplicates_file)
    verificar_y_filtrar(final_clean, archivo_validos, archivo_eliminados)

    # Cargar los artículos válidos para los siguientes requerimientos
    lista_articulos = cargar_articulos_bib_reqs(archivo_validos)
    if not lista_articulos:
        print("No se encontraron artículos válidos para continuar. Terminando ejecución.")
        return
    corpus_abstracts = [articulo['abstract'] for articulo in lista_articulos]

    # --- REQUERIMIENTO 2: Similitud Textual (Versión Automática) ---
    print("\n--- Ejecutando Requerimiento 2 (Automático) ---")
    if len(lista_articulos) >= 2:
        articulo1, articulo2 = lista_articulos[0], lista_articulos[1]
        print(f"Comparando Artículo 1: '{articulo1['title']}'")
        print(f"Y Artículo 2: '{articulo2['title']}'")
        
        # Levenshtein
        dist_lev = calcular_distancia_levenshtein(articulo1['abstract'][:500], articulo2['abstract'][:500])
        print(f"Distancia Levenshtein: {dist_lev}")
        # Jaccard
        sim_jac = calcular_similitud_jaccard(articulo1['abstract'], articulo2['abstract'])
        print(f"Similitud Jaccard: {sim_jac:.4f}")
        # TF-IDF
        sim_tfidf = calcular_similitud_tfidf_coseno(articulo1['abstract'], articulo2['abstract'], corpus_abstracts)
        print(f"Similitud TF-IDF: {sim_tfidf:.4f}")
        # BoW
        sim_bow = calcular_similitud_bow_coseno(articulo1['abstract'], articulo2['abstract'])
        print(f"Similitud Bag of Words: {sim_bow:.4f}")
        # SBERT
        print("Cargando modelo SBERT...")
        sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
        sim_sbert = calcular_similitud_sbert(articulo1['abstract'], articulo2['abstract'], sbert_model)
        print(f"Similitud SBERT: {sim_sbert:.4f}")
        # Doc2Vec
        print("Entrenando modelo Doc2Vec...")
        sim_d2v = calcular_similitud_doc2vec(articulo1['abstract'], articulo2['abstract'], corpus_abstracts)
        print(f"Similitud Doc2Vec: {sim_d2v:.4f}")
    else:
        print("No hay suficientes artículos para la comparación.")

    # --- REQUERIMIENTO 3: Frecuencia y Generación de Palabras Clave ---
    print("\n--- Ejecutando Requerimiento 3 ---")
    palabras_asociadas = ["Generative models", "Prompting", "Machine learning", "Multimodality", "Fine-tuning", "Training data", "Algorithmic bias", "Explainability", "Transparency", "Ethics", "Privacy", "Personalization", "Human-AI interaction", "AI literacy", "Co-creation"]
    frecuencias = calcular_frecuencia_palabras_asociadas(corpus_abstracts, palabras_asociadas)
    print("Frecuencia de Palabras Clave Predefinidas:")
    for palabra, freq in sorted(frecuencias.items(), key=lambda item: item[1], reverse=True):
        print(f"- {palabra}: {freq}")
    
    nuevas_palabras = generar_nuevas_palabras_tfidf(corpus_abstracts)
    print("\nNuevas Palabras Clave Generadas por TF-IDF:")
    for palabra in nuevas_palabras:
        print(f"- {palabra}")
    with open('keywords.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(nuevas_palabras))
    print("Nuevas palabras clave guardadas en 'keywords.txt'")

    # --- REQUERIMIENTO 4: Clustering Jerárquico ---
    print("\n--- Ejecutando Requerimiento 4 ---")
    num_articulos_demo = min(25, len(lista_articulos))
    articulos_demo = lista_articulos[:num_articulos_demo]
    corpus_demo = [a['abstract'] for a in articulos_demo]
    labels_demo = [f"{(a['title'][:75] + '...') if len(a['title']) > 75 else a['title']}" for a in articulos_demo]
    
    print(f"Usando {num_articulos_demo} artículos para los dendrogramas.")
    print("Cargando modelo SBERT para clustering...")
    sbert_model_cluster = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = sbert_model_cluster.encode(corpus_demo, show_progress_bar=True)
    
    for metodo in ['ward', 'complete', 'average']:
        realizar_clustering_y_graficar(embeddings, labels_demo, metodo, f"dendrograma_{metodo}.png")

    # --- REQUERimiento 5: Análisis Visual ---
    print("\n--- Ejecutando Requerimiento 5 ---")
    df_articulos = pd.DataFrame(bibtexparser.load(open(archivo_validos, encoding='utf-8')).entries)
    if not df_articulos.empty:
        generar_nube_de_palabras(df_articulos, "nube_de_palabras.png")
        generar_lineas_tiempo(df_articulos)
        generar_mapa_calor(df_articulos, "mapa_calor_autores.html")
        exportar_a_pdf("reporte_visual.pdf")
    else:
        print("No hay artículos en el DataFrame para el análisis visual.")
        
    print("\n--- EJECUCIÓN COMPLETA TERMINADA ---")

if __name__ == "__main__":
    # Ignorar advertencias para una salida más limpia
    warnings.filterwarnings("ignore", category=UserWarning, module='matplotlib')
    warnings.filterwarnings("ignore", category=FutureWarning)
    main()
