import json

# Suponiendo que el archivo JSON se llama "clima_ciudad.json" con utf-8
with open("clima_ciudad.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# 1. Determinar el pronóstico máximo de temperatura
temperaturas_horas = [registro['temperatura_c'] for registro in data['pronostico_proximas_horas']]
temperatura_maxima = max(temperaturas_horas)

# 2. Calcular el promedio de temperatura en las próximas horas
promedio_temperatura = round(sum(temperaturas_horas) / len(temperaturas_horas),2)

# 3. Obtener las condiciones meteorológicas esperadas y únicas
condiciones = list(set(registro['condicion'] for registro in data['pronostico_proximas_horas']))

# Resultados
print("Pronóstico máximo de temperatura:", temperatura_maxima, "°C")
print("Promedio de temperatura en las próximas horas:", promedio_temperatura, "°C")
print("Condiciones meteorológicas esperadas:", ", ".join(condiciones))
