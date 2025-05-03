import pandas as pd

# Cargar la base de datos
df = pd.read_excel("bd_clientes.xlsx")

# Convertir a string y limpiar formato
def limpiar_telefono(valor):
    try:
        # Convertir a int primero para eliminar .0, luego a str
        return str(int(float(valor))).strip()
    except:
        return ""

# 1. Eliminar datos en blanco (NaN) en las columnas "Nombre" y "Telefono"
df = df.dropna(subset=["nombre", "teléfono"])
df["teléfono"] = df["teléfono"].apply(limpiar_telefono)
# 2. Función para validar el formato de teléfono (debe comenzar con '3' y tener 10 dígitos)
def validar_telefono(telefono):
    telefono = str(telefono)  # Asegurarse de que el teléfono sea una cadena
    # Verificar si el teléfono comienza con '3' y tiene una longitud de 10 dígitos o es fijo 7 dígitos
    if (telefono.startswith("3") and len(telefono) == 10) or len(telefono) == 7:
        return True
    # Verifcar si es fijo

    return False

# 3. Aplicar la validación de teléfono
df["TelefonoValido"] = df["teléfono"].apply(validar_telefono)

# 4. Identificar si el teléfono es fijo o móvil (los fijos tienen más dígitos o un formato diferente)
def identificar_tipo_telefono(telefono):
    telefono = str(telefono)
    # Si el número tiene más de 10 dígitos, es fijo (asumimos que los fijos tienen más de 10 dígitos en Colombia)
    if len(telefono) == 7:
        return "Fijo"
    elif telefono.startswith("3") and len(telefono) == 10:
        return "Celular"
    return "Inválido"

# 5. Aplicar la función para identificar si es fijo o celular
df["TipoTelefono"] = df["teléfono"].apply(identificar_tipo_telefono)

# 6. Filtrar los registros con teléfonos válidos
df_validos = df[df["TelefonoValido"] == True]

# Mostrar los primeros registros para ver cómo quedaron
print(df_validos.head())

# Guardar el DataFrame limpio en un nuevo archivo
df_validos.to_excel("bd_clientes_limpia.xlsx", index=False)
