import pandas as pd




# Leer las hojas del archivo
archivo = "Reporte_Financiero_Q1_Generado.xlsx"

# Hoja de ingresos
ingresos = pd.read_excel(archivo, sheet_name="Ingresos_Q1", skiprows=2)

# Hoja de gastos
gastos = pd.read_excel(archivo, sheet_name="Gastos_Q1", skiprows=3)

# Calcular totales
total_ingresos = ingresos["Monto"].sum()
total_gastos = gastos["Valor_USD"].sum()
beneficio_bruto = total_ingresos - total_gastos

# Mostrar resultados
print("Total Ingresos:", round(total_ingresos, 2))
print("Total Gastos:", round(total_gastos, 2))
print( "Beneficio Bruto:", round(beneficio_bruto, 2))

# Análisis adicionales:
print("\nIngresos por categoría:")
print(ingresos.groupby("Categoría")["Monto"].sum().sort_values(ascending=False))

print("\nGastos por proveedor:")
print(gastos.groupby("Proveedor")["Valor_USD"].sum().sort_values(ascending=False))
