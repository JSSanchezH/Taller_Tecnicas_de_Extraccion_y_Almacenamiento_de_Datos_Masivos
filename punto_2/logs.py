import pandas as pd

# Cargar el archivo con el separador correcto
df = pd.read_csv("bd_logs_web.csv", sep=";", parse_dates=["Timestamp"])

# 1. Determinar cuál es el método HTTP más usado
metodo_mas_usado = df["MetodoHTTP"].value_counts().idxmax()
print("1. Método HTTP más usado:", metodo_mas_usado)

# 2. Determinar cuáles son las horas del día con mayor actividad (todas las horas ordenadas)
df["Hora"] = df["Timestamp"].dt.hour
actividad_por_hora = df["Hora"].value_counts().sort_index()
print("2. Actividad por hora del día:")
hora_max_actividad = actividad_por_hora.idxmax()
cantidad_max_actividad = actividad_por_hora.max()
print(f"\nLa hora con mayor actividad es {hora_max_actividad}:00 con {cantidad_max_actividad} solicitudes.")

# 3. Eliminar los registros que provengan del navegador "Opera"
df_sin_opera = df[~df["UserAgent"].str.contains("Opera", case=False, na=False)]
print("\n3. Registros después de eliminar los que usan Opera:")
print(df_sin_opera)

# 4. Evaluar la frecuencia de los códigos de estado
frecuencia_codigos = df["CodigoEstadoHTTP"].value_counts().sort_index()
print("\n4. Frecuencia de códigos de estado HTTP:")
print(frecuencia_codigos)

# 5. Calcular el porcentaje de éxito (2xx) vs errores (4xx)
total = len(df)
exitos = df["CodigoEstadoHTTP"].astype(str).str.startswith("2").sum()
errores = df["CodigoEstadoHTTP"].astype(str).str.startswith("4").sum()

porcentaje_exito = (exitos / total) * 100
porcentaje_errores = (errores / total) * 100

print("\n5. Porcentaje de éxito vs error:")
print(f"Éxito (2xx): {porcentaje_exito:.2f}%")
print(f"Errores (4xx): {porcentaje_errores:.2f}%")
