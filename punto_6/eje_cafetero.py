import requests
import pandas as pd

# Definir las coordenadas de las tres principales ciudades del Eje Cafetero
ciudades = {
    "Armenia": {"lat": 4.5333, "lon": -75.6813},
    "Manizales": {"lat": 5.0691, "lon": -75.5175},
    "Pereira": {"lat": 4.8134, "lon": -75.6969}
}

# URL base de la API Open-Meteo para obtener el pronóstico
url = "https://api.open-meteo.com/v1/forecast"

# Lista para almacenar los resultados
resultados = []

# Iterar sobre las ciudades y obtener los datos meteorológicos
for ciudad, coordenadas in ciudades.items():
    params = {
        "latitude": coordenadas["lat"],
        "longitude": coordenadas["lon"],
        "hourly": "temperature_2m,windspeed_10m,precipitation,relativehumidity_2m,cloudcover", # Agregamos humedad y nubosidad
        "timezone": "America/Bogota"
    }

    # Enviar la solicitud a la API
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        # Verificamos si los datos de la ciudad existen
        if "hourly" in data:
            temperaturas = data["hourly"]["temperature_2m"]
            velocidades_viento = data["hourly"]["windspeed_10m"]
            precipitaciones = data["hourly"]["precipitation"]
            humedades = data["hourly"]["relativehumidity_2m"] # Obtenemos la humedad
            nubosidades = data["hourly"]["cloudcover"] # Obtenemos la nubosidad
            tiempos = data["hourly"]["time"]

            # Almacenar los resultados en la lista
            for i in range(len(temperaturas)):
                resultados.append({
                    "Ciudad": ciudad,
                    "Fecha": tiempos[i],
                    "Temperatura (°C)": temperaturas[i],
                    "Velocidad del Viento (m/s)": velocidades_viento[i],
                    "Precipitación (mm)": precipitaciones[i],
                    "Humedad Relativa (%)": humedades[i], # Agregamos la humedad al diccionario
                    "Nubosidad (%)": nubosidades[i] # Agregamos la nubosidad al diccionario
                })
        else:
            print(f"No se encontraron datos horarios para {ciudad}")
    else:
        print(f"Error al obtener datos para {ciudad} - Status Code: {response.status_code}")

# Crear un DataFrame de los resultados
df = pd.DataFrame(resultados)

# Convertir la columna 'Fecha' al tipo datetime de pandas
df['Fecha'] = pd.to_datetime(df['Fecha'])

# Crear las nuevas columnas de año, mes, día y hora
df['Año'] = df['Fecha'].dt.year
df['Mes'] = df['Fecha'].dt.month
df['Día'] = df['Fecha'].dt.day
df['Hora'] = df['Fecha'].dt.hour

# Guardar el DataFrame en un archivo CSV
df.to_csv("datos_meteorologicos_eje_cafetero.csv", index=False)

print("Datos meteorológicos guardados correctamente.")