import requests
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os
from dotenv import load_dotenv, find_dotenv

# Cargar las variables de entorno desde el archivo .env (busca en el directorio actual y superiores)
load_dotenv(find_dotenv())

# Obtener la clave de API desde la variable de entorno
API_KEY = os.environ.get("NASA_API_KEY")

# Verificar si la clave de API está definida
if not API_KEY:
    print("Error: La variable de entorno NASA_API_KEY no está definida en el archivo .env.")
    exit()

# URL de la API de APOD
URL = "https://api.nasa.gov/planetary/apod"

# Función para obtener los datos de la NASA (APOD)
def obtener_datos_apod(fecha):
    params = {
        "api_key": API_KEY,
        "date": fecha
    }
    print(f"Enviando solicitud a: {URL}?{'&'.join([f'{k}={v}' for k, v in params.items()])}")
    response = requests.get(URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener datos para {fecha}: {response.status_code}")
        return None

# Crear un motor de SQLAlchemy para almacenar los datos en SQLite
engine = create_engine('sqlite:///nasa_apod.db', echo=True)

# Definir las columnas para almacenar
columns = ['fecha', 'titulo', 'descripcion', 'url_imagen', 'hdurl_imagen']

# Crear un DataFrame vacío para almacenar los datos
df_apod = pd.DataFrame(columns=columns)

# Definir el rango de fechas (por ejemplo, los últimos 7 días)
fecha_inicio = datetime(2025, 5, 1)
fecha_fin = datetime(2025, 5, 7)

# Iterar sobre las fechas y obtener los datos de la API
for n in range((fecha_fin - fecha_inicio).days + 1):
    fecha_actual = fecha_inicio + pd.Timedelta(n, 'D')
    fecha_str = fecha_actual.strftime('%Y-%m-%d')

    # Obtener los datos de la NASA
    data = obtener_datos_apod(fecha_str)

    if data:
        # Extraer la información y agregarla al DataFrame
        df_apod = pd.concat([df_apod, pd.DataFrame([{
            'fecha': fecha_str,
            'titulo': data['title'],
            'descripcion': data['explanation'],
            'url_imagen': data['url'],
            'hdurl_imagen': data.get('hdurl', None)  # Algunas imágenes no tienen hdurl
        }])], ignore_index=True)

# Almacenar el DataFrame en la base de datos SQLite
df_apod.to_sql('apod', con=engine, if_exists='replace', index=False)

print("Datos de APOD guardados correctamente en la base de datos.")