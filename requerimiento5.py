import bibtexparser
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import plotly.express as px
import pycountry_convert as pc
import re
import os
from fpdf import FPDF

def cargar_articulos_bib(ruta_archivo):
    """
    Carga artículos desde un archivo .bib y extrae campos relevantes.
    """
    with open(ruta_archivo, 'r', encoding='utf-8') as bibfile:
        bib_database = bibtexparser.load(bibfile)
    df = pd.DataFrame(bib_database.entries)
    return df

def generar_nube_de_palabras(df, file_name):
    """
    Genera y guarda una nube de palabras a partir de los abstracts y keywords.
    """
    print("\n--- Generando Nube de Palabras ---")
    text_abstracts = ' '.join(df['abstract'].fillna(''))
    text_keywords = ' '.join(df['keywords'].fillna(''))
    full_text = text_abstracts + ' ' + text_keywords
    if not full_text.strip():
        print("No hay texto disponible para generar la nube de palabras.")
        return
    stopwords = set(STOPWORDS)
    stopwords.update(["research", "paper", "study", "results", "approach", "method", "based", "model", "data", "analysis", "system"])
    wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=stopwords, min_font_size=10, colormap='viridis').generate(full_text)
    plt.figure(figsize=(10, 5), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    try:
        plt.savefig(file_name, dpi=300)
        print(f"Nube de palabras guardada en: {file_name}")
    except Exception as e:
        print(f"Error al guardar el archivo {file_name}: {e}")
    plt.close()

def generar_lineas_tiempo(df):
    """
    Genera y guarda gráficos de barras para publicaciones por año y por revista/conferencia.
    """
    print("\n--- Generando Gráficos de Líneas de Tiempo ---")
    if 'year' in df.columns:
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        pub_por_ano = df['year'].value_counts().sort_index()
        plt.figure(figsize=(10, 6))
        pub_por_ano.plot(kind='bar', color='skyblue')
        plt.title('Número de Publicaciones por Año')
        plt.xlabel('Año')
        plt.ylabel('Número de Publicaciones')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--')
        plt.tight_layout()
        plt.savefig("linea_temporal_año.png", dpi=300)
        print("Gráfico de publicaciones por año guardado en: linea_temporal_año.png")
        plt.close()
    else:
        print("No se encontró la columna 'year' para generar el gráfico por año.")
    df['venue'] = df['journal'].fillna(df['booktitle'])
    if not df['venue'].dropna().empty:
        pub_por_venue = df['venue'].value_counts().nlargest(10)
        plt.figure(figsize=(10, 8))
        pub_por_venue.sort_values().plot(kind='barh', color='lightcoral')
        plt.title('Top 10 Revistas/Conferencias por Número de Publicaciones')
        plt.xlabel('Número de Publicaciones')
        plt.ylabel('Revista o Conferencia')
        plt.tight_layout()
        plt.savefig("publicaciones_por_revista.png", dpi=300)
        print("Gráfico de publicaciones por revista guardado en: publicaciones_por_revista.png")
        plt.close()
    else:
        print("No se encontraron datos de 'journal' o 'booktitle' para generar el gráfico por revista.")

def generar_mapa_calor(df, file_name):
    """
    Genera un mapa de calor geográfico basado en el país del primer autor.
    """
    print("\n--- Generando Mapa de Calor Geográfico ---")
    if 'author' not in df.columns:
        print("No se encontró la columna 'author' para generar el mapa de calor.")
        return
    country_mapping = {"USA": "United States", "UK": "United Kingdom", "UAE": "United Arab Emirates", "Korea": "South Korea", "Peoples R China": "China"}
    def get_country_from_affiliation(affiliation):
        if not isinstance(affiliation, str):
            return None
        possible_country = affiliation.split(',')[-1].strip()
        possible_country = re.sub(r'[^A-Za-z ]+', '', possible_country)
        if possible_country in country_mapping:
            return country_mapping[possible_country]
        try:
            country_code = pc.country_name_to_country_alpha2(possible_country, cn_name_format="default")
            return pc.country_alpha2_to_country_name(country_code)
        except Exception:
            return None
    df['country'] = df['author'].apply(get_country_from_affiliation)
    country_counts = df['country'].value_counts().reset_index()
    country_counts.columns = ['country', 'publications']
    if country_counts.empty:
        print("No se pudo extraer información de países para generar el mapa.")
        return
    def country_to_iso_alpha3(country_name):
        try:
            return pc.country_name_to_country_alpha3(country_name)
        except Exception:
            return None
    country_counts['iso_alpha'] = country_counts['country'].apply(country_to_iso_alpha3)
    country_counts = country_counts.dropna(subset=['iso_alpha'])
    fig = px.choropleth(country_counts, locations="iso_alpha", color="publications", hover_name="country", color_continuous_scale=px.colors.sequential.Plasma, title="Distribución Geográfica de Publicaciones por Primer Autor")
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    try:
        fig.write_html(file_name)
        print(f"Mapa de calor guardado en: {file_name}")
    except Exception as e:
        print(f"Error al guardar el archivo {file_name}: {e}")

def exportar_a_pdf(file_name):
    """
    Exporta las visualizaciones generadas a un único archivo PDF.
    """
    print("\n--- Exportando reporte a PDF ---")
    pdf = FPDF()
    image_files = ["nube_de_palabras.png", "linea_temporal_año.png", "publicaciones_por_revista.png"]
    titles = ["1. Nube de Palabras Clave", "2.a. Publicaciones por Año", "2.b. Top 10 Revistas/Conferencias"]
    
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Reporte de Análisis Bibliométrico', 0, 1, 'C')
    pdf.ln(10)

    for i, image_file in enumerate(image_files):
        if os.path.exists(image_file):
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, titles[i], 0, 1)
            # A4 width is 210mm, margins 10mm each side -> 190mm available
            pdf.image(image_file, x=10, w=190)
            pdf.ln(5)
        else:
            pdf.set_font('Arial', 'I', 12)
            pdf.cell(0, 10, f"No se pudo generar la imagen: {image_file}", 0, 1)
            pdf.ln(10)

    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, '3. Distribución Geográfica de Autores', 0, 1)
    pdf.set_font('Arial', '', 11)
    if os.path.exists("mapa_calor_autores.html"):
        pdf.multi_cell(0, 10, 'El mapa de calor es un gráfico interactivo y ha sido guardado como un archivo HTML. Por favor, abra el siguiente archivo en un navegador web para explorarlo:')
        pdf.ln(5)
        pdf.set_text_color(0, 0, 255)
        pdf.set_font('Arial', 'U', 11)
        pdf.cell(0, 10, 'mapa_calor_autores.html', 0, 1)
    else:
        pdf.multi_cell(0, 10, 'No se pudo generar el archivo del mapa de calor.')

    try:
        pdf.output(file_name)
        print(f"Reporte PDF guardado en: {file_name}")
    except Exception as e:
        print(f"Error al guardar el archivo PDF {file_name}: {e}")

if __name__ == "__main__":
    print("--- Requerimiento 5: Análisis Visual de Producción Científica ---")
    ruta_bib = 'archivos/articulos_con_titulo_y_abstract.bib'
    print(f"\nCargando artículos desde: {ruta_bib}")
    df_articulos = cargar_articulos_bib(ruta_bib)
    if not df_articulos.empty:
        print(f"Se cargaron {len(df_articulos)} artículos.")
        generar_nube_de_palabras(df_articulos, "nube_de_palabras.png")
        generar_lineas_tiempo(df_articulos)
        generar_mapa_calor(df_articulos, "mapa_calor_autores.html")
        exportar_a_pdf("reporte_visual.pdf")
    else:
        print("No se encontraron artículos en el archivo especificado.")
