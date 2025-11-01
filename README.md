# Proyecto de Análisis Bibliométrico

Este proyecto implementa una serie de algoritmos para el análisis bibliométrico y computacional sobre un dominio de conocimiento, a partir de un conjunto de datos de publicaciones científicas en formato `.bib`.

El análisis cubre la comparación de similitud de textos, la extracción de palabras clave, el clustering jerárquico y la generación de visualizaciones para el análisis de la producción científica.

## Características

- **Análisis de Similitud Textual (Req. 2):** Compara resúmenes (abstracts) de artículos utilizando 6 algoritmos diferentes, incluyendo clásicos (Levenshtein, Jaccard, TF-IDF, BoW) y modelos de IA (Sentence-BERT, Doc2Vec).
- **Análisis de Frecuencia (Req. 3):** Calcula la frecuencia de palabras clave predefinidas y genera una nueva lista de términos relevantes mediante TF-IDF.
- **Clustering Jerárquico (Req. 4):** Agrupa artículos basados en la similitud semántica de sus abstracts y genera dendrogramas para visualizar los clusters.
- **Visualización de Datos (Req. 5):** Crea un conjunto de visualizaciones que incluyen una nube de palabras, líneas de tiempo de publicación, un mapa de calor geográfico y exporta los resultados a un reporte en PDF.

## Instalación

Sigue estos pasos para configurar el entorno y ejecutar el proyecto.

1.  **Prerrequisitos:**
    - Asegúrate de tener Python 3.8 o superior instalado.

2.  **Clonar el Repositorio (Opcional):**
    ```bash
    git clone <URL-del-repositorio>
    cd <nombre-del-directorio>
    ```

3.  **Instalar Dependencias:**
    Todas las librerías necesarias están listadas en el archivo `requirements.txt`. Para instalarlas, ejecuta el siguiente comando en tu terminal:
    ```bash
    pip install -r requirements.txt
    ```
    *Nota: La instalación puede tardar varios minutos debido al tamaño de las librerías de IA como PyTorch.*

## Uso

Cada requerimiento funcional ha sido implementado en su propio script de Python. A continuación se detalla cómo ejecutar cada uno y qué resultados produce.

### Requerimiento 1: Preprocesamiento de Datos

Este requerimiento fue completado por el usuario. Se asume que los scripts `aplication.py` o `requerimiento1.py` se encargan de tomar los datos crudos de las carpetas `archivos/descargaACM` y `archivos/descargaScienceDirect` y producir el archivo unificado `archivos/articulos_con_titulo_y_abstract.bib`, que es la entrada para los demás scripts.

### Requerimiento 2: Algoritmos de Similitud Textual

Este script demuestra 6 algoritmos de similitud comparando los dos primeros artículos del corpus.

-   **Comando:**
    ```bash
    python requerimiento2.py
    ```
-   **Salida:**
    - Muestra en la consola los resultados de similitud para cada uno de los 6 algoritmos.
    - Las explicaciones detalladas de cada algoritmo se encuentran como comentarios dentro del propio script.

### Requerimiento 3: Análisis de Frecuencia de Palabras Clave

Este script analiza la frecuencia de un conjunto predefinido de palabras clave y genera una nueva lista de términos relevantes.

-   **Comando:**
    ```bash
    python requerimiento3.py
    ```
-   **Salida:**
    - Muestra en la consola la frecuencia de las palabras clave originales.
    - Muestra una nueva lista de 15 palabras clave generadas con TF-IDF.
    - Calcula y muestra una métrica de "precisión" que compara ambas listas.

### Requerimiento 4: Clustering Jerárquico

Este script agrupa los artículos según el significado de sus abstracts y crea visualizaciones en forma de árbol (dendrogramas).

-   **Comando:**
    ```bash
    python requerimiento4.py
    ```
-   **Salida:**
    - Genera 3 archivos de imagen en la raíz del proyecto:
        - `dendrograma_ward.png`
        - `dendrograma_complete.png`
        - `dendrograma_average.png`

### Requerimiento 5: Análisis Visual y Reporte

Este script genera un conjunto de visualizaciones sobre la producción científica y las compila en un reporte PDF.

-   **Comando:**
    ```bash
    python requerimiento5.py
    ```
-   **Salida:**
    - Genera 4 archivos de visualización en la raíz del proyecto:
        - `nube_de_palabras.png`
        - `linea_temporal_año.png`
        - `publicaciones_por_revista.png`
        - `mapa_calor_autores.html` (mapa interactivo, abrir en un navegador).
    - Genera un archivo PDF que consolida todos los resultados:
        - `reporte_visual.pdf`

## Autor

-   [Tu Nombre]
