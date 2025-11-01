import bibtexparser
import re
import itertools
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def cargar_abstracts(bib_file):
    """Carga abstracts desde un archivo .bib."""
    with open(bib_file, 'r', encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    
    abstracts = []
    for entry in bib_database.entries:
        if 'abstract' in entry:
            abstracts.append(entry['abstract'])
    return abstracts

def extraer_terminos_relevantes(abstracts, num_terminos=50):
    """Extrae términos relevantes usando TF-IDF."""
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_df=0.85, min_df=3)
    tfidf_matrix = vectorizer.fit_transform(abstracts)
    feature_names = np.array(vectorizer.get_feature_names_out())
    sum_tfidf = tfidf_matrix.sum(axis=0)
    scores = [(feature_names[col], sum_tfidf[0, col]) for col in range(tfidf_matrix.shape[1])]
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    mejores_terminos = [termino for termino, puntaje in sorted_scores[:num_terminos]]
    return mejores_terminos

def construir_grafo_coocurrencia(terminos, abstracts):
    """Construye un grafo de co-ocurrencia de términos."""
    G = nx.Graph()
    for termino in terminos:
        G.add_node(termino)

    for abstract in abstracts:
        # Buscamos qué términos de nuestra lista aparecen en el abstract
        terminos_en_abstract = []
        for termino in terminos:
            # Usamos \b para encontrar la palabra exacta
            if re.search(r'\b' + re.escape(termino) + r'\b', abstract, re.IGNORECASE):
                terminos_en_abstract.append(termino)
        
        # Añadimos una arista por cada par de términos que co-ocuren
        for term1, term2 in itertools.combinations(terminos_en_abstract, 2):
            if G.has_edge(term1, term2):
                G[term1][term2]['weight'] += 1
            else:
                G.add_edge(term1, term2, weight=1)
    return G

def analizar_grafo(G):
    """Calcula el grado de los nodos y las componentes conexas."""
    # Calcular el grado de cada nodo
    grados = dict(G.degree())
    # Ordenar los términos por su grado (de mayor a menor)
    terminos_mas_conectados = sorted(grados.items(), key=lambda item: item[1], reverse=True)
    
    # Encontrar componentes conexas
    componentes = list(nx.connected_components(G))
    
    return terminos_mas_conectados, componentes

if __name__ == "__main__":
    print("--- Requerimiento 2 (Grafos): Análisis de Co-ocurrencia de Términos ---")
    
    # Cargar abstracts
    bib_file_path = r'Seguimiento2\articulos_con_titulo_y_abstract.bib'
    abstracts = cargar_abstracts(bib_file_path)
    
    if abstracts:
        print(f"Se cargaron {len(abstracts)} abstracts.")
        
        # Extraer los términos más relevantes del corpus
        terminos_clave = extraer_terminos_relevantes(abstracts, num_terminos=50)
        print(f"\nSe extrajeron {len(terminos_clave)} términos clave usando TF-IDF.")

        # Construir el grafo de co-ocurrencia
        grafo_coocurrencia = construir_grafo_coocurrencia(terminos_clave, abstracts)
        print(f"Grafo de co-ocurrencia construido con {grafo_coocurrencia.number_of_nodes()} nodos y {grafo_coocurrencia.number_of_edges()} aristas.")

        # Analizar el grafo
        # --- PASO ADICIONAL: FILTRAR ARISTAS DÉBILES ---
        # Eliminar aristas con un peso bajo para reducir la densidad y mejorar la visualización.
        # Puedes ajustar este umbral. Un valor más alto hará el grafo más escaso.
        umbral_peso = 5  # Por ejemplo, mantener solo conexiones que ocurrieron 5 o más veces.
        aristas_a_eliminar = [(u, v) for u, v, data in grafo_coocurrencia.edges(data=True) if data['weight'] < umbral_peso]
        grafo_coocurrencia.remove_edges_from(aristas_a_eliminar)
        # Eliminar nodos que quedaron aislados después de quitar aristas
        grafo_coocurrencia.remove_nodes_from(list(nx.isolates(grafo_coocurrencia)))
        print(f"Grafo filtrado: {grafo_coocurrencia.number_of_nodes()} nodos y {grafo_coocurrencia.number_of_edges()} aristas (peso > {umbral_peso-1}).")

        terminos_centrales, componentes_tematicas = analizar_grafo(grafo_coocurrencia)
        
        # Mostrar los términos más conectados
        print("\n--- Términos más conectados (mayor grado) ---")
        for termino, grado in terminos_centrales[:10]:
            print(f"- '{termino}' (Grado: {grado})")
            
        # Mostrar las componentes conexas (temas)
        print("\n--- Grupos de Términos Conectados (Temas Detectados) ---")
        componentes_grandes = [c for c in componentes_tematicas if len(c) > 2]
        if componentes_grandes:
            for i, comp in enumerate(componentes_grandes, 1):
                print(f"Tema {i}: {list(comp)}")
        else:
            print("No se encontraron grupos temáticos significativos (componentes con más de 2 términos).")

        # Opcional: Guardar el grafo para visualización
        output_graph_path = 'grafo_coocurrencia.graphml'
        nx.write_graphml(grafo_coocurrencia, output_graph_path)
        print(f"\nGrafo guardado en formato GraphML en: {output_graph_path}")

    else:
        print("No se encontraron abstracts en el archivo especificado.")
