import bibtexparser
import networkx as nx
import numpy as np
import itertools
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def cargar_articulos(bib_file):
    """Carga artículos desde un archivo .bib."""
    with open(bib_file, encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    return bib_database.entries

def construir_grafo_citaciones(articulos, inferir_por_similitud=True, top_n_similares=3):
    """
    Construye un grafo de citaciones.
    1. Usa citaciones explícitas si existen (campo 'cites').
    2. Opcionalmente, infiere citaciones por similitud de texto.
    """
    G = nx.DiGraph()
    
    # Mapeo de ID a entrada de artículo para fácil acceso
    articulos_por_id = {art.get('ID'): art for art in articulos if 'ID' in art}

    # --- PASO 1: Añadir nodos y procesar citaciones explícitas ---
    for articulo in articulos:
        node_id = articulo.get('ID', articulo.get('title', 'N/A')[:30])
        if not G.has_node(node_id):
            G.add_node(node_id, title=articulo.get('title', 'Sin título'))
        
        # Si el artículo tiene un campo 'cites', se añaden las aristas directas
        if 'cites' in articulo:
            # El campo 'cites' debería ser una cadena de IDs separados por comas
            citados_ids = [c.strip() for c in articulo['cites'].split(',')]
            for citado_id in citados_ids:
                if citado_id in articulos_por_id:
                    # El artículo actual (node_id) cita a 'citado_id'
                    if not G.has_node(citado_id):
                         G.add_node(citado_id, title=articulos_por_id[citado_id].get('title', 'Sin título'))
                    G.add_edge(node_id, citado_id, weight=1.0, type='explicita') # Peso 1.0 para citaciones explícitas

    # --- PASO 2: Inferir citaciones por similitud (si está activado) ---
    if inferir_por_similitud and len(articulos) > 1:
        ids = [art.get('ID', art.get('title', 'N/A')[:30]) for art in articulos]
        years = [int(art.get('year', '0')) for art in articulos]
        textos = [art.get('title', '') + ' ' + art.get('abstract', '') for art in articulos]

        # Vectorizar todos los textos de una vez (mucho más eficiente)
        vectorizer = TfidfVectorizer(stop_words='english', min_df=2)
        tfidf_matrix = vectorizer.fit_transform(textos)

        # Calcular la matriz de similitud del coseno para todos contra todos
        matriz_similitud = cosine_similarity(tfidf_matrix)
        np.fill_diagonal(matriz_similitud, 0) # Un artículo no puede ser similar a sí mismo

        # Para cada artículo, encuentra sus N más similares y añade las aristas
        for i in range(len(articulos)):
            # Obtiene los índices de los artículos más similares, ordenados de mayor a menor
            indices_similares = np.argsort(matriz_similitud[i])[-top_n_similares:][::-1]

            for j in indices_similares:
                similitud = matriz_similitud[i, j]
                # Solo añadir si no existe ya una arista explícita
                if similitud > 0 and not G.has_edge(ids[i], ids[j]) and not G.has_edge(ids[j], ids[i]):
                    # Infiere la dirección por el año de publicación
                    # El más nuevo (i) cita al más antiguo (j)
                    if years[i] > years[j]:
                        G.add_edge(ids[i], ids[j], weight=similitud, type='inferida')
                    else: # Si son del mismo año o el otro es más nuevo, la dirección es inversa
                        G.add_edge(ids[j], ids[i], weight=similitud, type='inferida')
    return G

def encontrar_camino_minimo(G, origen, destino):
    """Encuentra el camino mínimo entre dos nodos usando Dijkstra."""
    try:
        # Invertimos el peso porque Dijkstra busca el camino de menor suma
        # y nosotros queremos el de mayor similitud.
        path = nx.dijkstra_path(G, source=origen, target=destino, weight=lambda u, v, d: 1 - d['weight'])
        return path
    except nx.NetworkXNoPath:
        return f"No hay un camino entre {origen} y {destino}."
    except nx.NodeNotFound:
        return f"Uno de los nodos no se encuentra en el grafo."

def encontrar_componentes_fuertemente_conexas(G):
    """Encuentra y devuelve las componentes fuertemente conexas del grafo."""
    return list(nx.strongly_connected_components(G))

if __name__ == "__main__":
    # Ruta al archivo de artículos únicos
    bib_file_path = r'Seguimiento2\articulos_con_titulo_y_abstract.bib'
    
    # Cargar los artículos
    articulos = cargar_articulos(bib_file_path)
    
    # Construir el grafo de citaciones
    grafo_citaciones = construir_grafo_citaciones(articulos, inferir_por_similitud=True)
    
    print(f"Grafo construido con {grafo_citaciones.number_of_nodes()} nodos y {grafo_citaciones.number_of_edges()} aristas.")
    
    # --- PASO 3: Analizar la conectividad de la red ---
    print("\n--- Análisis de Conectividad de la Red ---")
    if grafo_citaciones.number_of_nodes() > 1:
        
        G_undirected = grafo_citaciones.to_undirected()
        
        # Encontrar todos los componentes conectados
        componentes_conectados = list(nx.connected_components(G_undirected))
        
        if componentes_conectados:
            print(f"Se encontraron {len(componentes_conectados)} componentes conectados (grupos de artículos).")
            
            # Encontrar el componente más grande (a menudo llamado el "componente gigante")
            componente_gigante_nodos = max(componentes_conectados, key=len)
            
            # Crear un subgrafo que solo contiene el componente gigante
            componente_gigante_grafo = grafo_citaciones.subgraph(componente_gigante_nodos)
            
            print(f"El componente conectado más grande tiene {componente_gigante_grafo.number_of_nodes()} nodos y {componente_gigante_grafo.number_of_edges()} aristas.")
            
            if nx.is_strongly_connected(componente_gigante_grafo):
                print("El componente gigante es fuertemente conectado. Calculando métricas de conectividad:")
                
                # Calcular el diámetro del componente (el camino más largo de los caminos más cortos)
                # Usa Dijkstra o Floyd-Warshall internamente.
                diametro = nx.diameter(componente_gigante_grafo, weight='weight')
                print(f"  - Diámetro de la red (basado en similitud): {diametro:.4f}")

                # Calcular el promedio de las longitudes de los caminos mínimos
                promedio_camino = nx.average_shortest_path_length(componente_gigante_grafo, weight='weight')
                print(f"  - Longitud promedio del camino mínimo: {promedio_camino:.4f}")
            else:
                print("El componente gigante no es fuertemente conectado, por lo que no se puede calcular un único diámetro o promedio de caminos para todo el componente.")
                # Podríamos analizar las componentes fuertemente conexas DENTRO del componente gigante si fuera necesario.

        else:
            print("No se encontraron componentes conectados en el grafo.")

    # Encontrar y mostrar componentes fuertemente conexas
    print("\nBuscando componentes fuertemente conexas:")
    componentes = encontrar_componentes_fuertemente_conexas(grafo_citaciones)
    
    if componentes:
        print(f"Se encontraron {len(componentes)} componentes fuertemente conexas.")
        # Imprimimos solo las componentes con más de un artículo
        componentes_relevantes = [c for c in componentes if len(c) > 1]
        if componentes_relevantes:
            print("Componentes con más de un artículo:")
            for i, comp in enumerate(componentes_relevantes, 1):
                print(f"  Componente {i}: {list(comp)}")
        else:
            print("No se encontraron componentes con más de un artículo.")
    else:
        print("No se encontraron componentes fuertemente conexas.")

    # Opcional: Guardar el grafo para visualización
    output_graph_path = 'grafo_citaciones.graphml'
    nx.write_graphml(grafo_citaciones, output_graph_path)
    print(f"\nGrafo guardado en formato GRAPHML en: {output_graph_path}")
