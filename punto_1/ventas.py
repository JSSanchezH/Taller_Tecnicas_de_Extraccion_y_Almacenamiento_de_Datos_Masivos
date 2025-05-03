import pandas as pd

# Cargar datos
df = pd.read_csv("bd_ventas.csv", parse_dates=["Fecha"])

# 1. Cuántos productos se vendieron en febrero de 2025
ventas_febrero_2025 = df[(df["Fecha"].dt.month == 2) & (df["Fecha"].dt.year == 2025)]["Cantidad"].sum()
print("1. Productos vendidos en febrero de 2025:", ventas_febrero_2025)

# 2. Promedio mensual de ventas (sin restringir por año)
df["Mes"] = df["Fecha"].dt.to_period("M")
promedio_mensual = df.groupby("Mes")["Cantidad"].sum().mean()
print("2. Promedio mensual de ventas:", promedio_mensual)

# 3. Venta más alta registrada en enero (cualquier año)
enero_df = df[df["Fecha"].dt.month == 1].copy()
enero_df["TotalVenta"] = enero_df["Cantidad"] * enero_df["PrecioUnitario"]
venta_max_enero = enero_df.loc[enero_df["TotalVenta"].idxmax()]
print("\n3. Venta más alta registrada en enero:")
print("Producto:", venta_max_enero["Nombre"])
print("Cantidad:", venta_max_enero["Cantidad"])
print("Precio Unitario:", venta_max_enero["PrecioUnitario"])
print("Total Venta:", venta_max_enero["TotalVenta"])
print("Fecha:", venta_max_enero["Fecha"].date())

# 4. Día con mayor cantidad de ventas en el primer trimestre (enero-marzo, sin importar el año)
q1_df = df[df["Fecha"].dt.month.isin([1, 2, 3])]
ventas_por_dia = q1_df.groupby("Fecha")["Cantidad"].sum()
dia_max_ventas = ventas_por_dia.idxmax()
print("\n4. Día con mayor cantidad de ventas en el primer trimestre:")
print("Fecha:", dia_max_ventas.date())
print("Cantidad de productos vendidos:", ventas_por_dia.max())

def agregar_registro(df, nuevo_registro, archivo_salida):
    """
    Agrega un nuevo registro de venta al DataFrame y guarda el resultado en un archivo CSV.
    """
    nuevo_df = pd.DataFrame([nuevo_registro])
    nuevo_df["Fecha"] = pd.to_datetime(nuevo_df["Fecha"])
    df_actualizado = pd.concat([df, nuevo_df], ignore_index=True)
    df_actualizado.to_csv(archivo_salida, index=False)
    print("Registro agregado exitosamente. Guardado en:", archivo_salida)
    return df_actualizado

nuevo = {
    "ID_Producto": "CEL010",
    "Nombre": "Samsung Galaxy A55",
    "Cantidad": 2,
    "PrecioUnitario": 399.99,
    "Fecha": "2025-04-15"
}

df = agregar_registro(df, nuevo, "ventas_actualizado.csv")

def eliminar_registros(df, condicion, archivo_salida):
    """
    Elimina filas del DataFrame según una condición booleana y guarda el resultado en un archivo CSV.
    """
    df_filtrado = df[~condicion(df)].copy()
    df_filtrado.to_csv(archivo_salida, index=False)
    print("Registros eliminados según la condición. Guardado en:", archivo_salida)
    return df_filtrado

# Ejemplo de uso:
# Eliminar productos cuya cantidad sea menor a 3
condicion = lambda df: df["Cantidad"] < 3
df = eliminar_registros(df, condicion, "ventas_filtradas.csv")
