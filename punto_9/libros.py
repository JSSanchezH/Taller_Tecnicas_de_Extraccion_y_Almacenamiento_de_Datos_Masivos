import requests
from bs4 import BeautifulSoup
import pandas as pd

# Función para obtener los datos de una página
def obtener_datos_pagina(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    else:
        print(f"Error al obtener la página: {response.status_code}")
        return None

# Función para extraer la información de cada libro
def obtener_libros(soup):
    libros = []
    # Encontramos todos los contenedores de los libros
    for libro in soup.find_all('article', class_='product_pod'):
        titulo = libro.find('h3').find('a')['title']
        precio = libro.find('p', class_='price_color').text
        disponibilidad = libro.find('p', class_='instock availability').text.strip()
        rating = libro.find('p', class_='star-rating')['class'][1]  # Clases: 'One', 'Two', 'Three', 'Four', 'Five'
        enlace = libro.find('h3').find('a')['href']
        
        libros.append({
            'Título': titulo,
            'Precio': precio,
            'Disponibilidad': disponibilidad,
            'Rating': rating,
            'Enlace': f"https://books.toscrape.com/catalogue/{enlace}",
        })
    return libros

# Función para obtener todas las páginas de libros
def obtener_todos_los_libros():
    url_base = "https://books.toscrape.com/catalogue/page-{page}.html"
    libros_totales = []
    page = 1
    
    while True:
        url = url_base.format(page=page)
        soup = obtener_datos_pagina(url)
        
        if soup:
            libros = obtener_libros(soup)
            if libros:
                libros_totales.extend(libros)
                page += 1
            else:
                break
        else:
            break

    return libros_totales

# Obtener todos los libros
libros = obtener_todos_los_libros()

# Crear un DataFrame de pandas para almacenar los datos
df_libros = pd.DataFrame(libros)

# Guardar los datos en un archivo CSV
df_libros.to_csv('libros_toscrape.csv', index=False)

print("Datos de los libros guardados correctamente.")
