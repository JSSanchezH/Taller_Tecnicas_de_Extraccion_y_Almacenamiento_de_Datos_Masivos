import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL base
url_base = "https://quotes.toscrape.com/page/{}/"

# Lista para almacenar las citas
citas = []

# Empezar desde la página 1
pagina = 1

while True:
    url = url_base.format(pagina)
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Fin de las páginas o error en la página {pagina}")
        break

    soup = BeautifulSoup(response.content, "html.parser")
    bloques_citas = soup.find_all("div", class_="quote")

    if not bloques_citas:
        break  # No hay más citas

    for bloque in bloques_citas:
        texto = bloque.find("span", class_="text").get_text()
        autor = bloque.find("small", class_="author").get_text()
        etiquetas = [tag.get_text() for tag in bloque.find_all("a", class_="tag")]

        citas.append({
            "Cita": texto,
            "Autor": autor,
            "Etiquetas": ", ".join(etiquetas)
        })

    pagina += 1

# Convertir a DataFrame y guardar
df_citas = pd.DataFrame(citas)

# El quoting=1 evita que las ";" de las citas corran una columna el csv
df_citas.to_csv("citas_extraidas.csv", index=False, encoding="utf-8", quoting=1)

print("Extracción completada. Se guardaron todas las citas en 'citas_extraidas.csv'.")
