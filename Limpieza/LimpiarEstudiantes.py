import pandas as pd

# ruta
archivo = "TablasIniciales/Tabla_estudiantes_7moa9no.xlsx"

# cargar
df = pd.read_excel(archivo)

# normalizar nombres de columnas
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# --- NUEVA UBICACIÓN PARA dropna() ---
# Lista de las columnas a verificar por valores nulos (usando los nombres normalizados)
columnas_a_verificar = [
    "cr_total_dias_ingreso",
    "primera_conexion_crea",
    "dias_de_conexion_dispositivo",
    "primera_conexion_dispositivo"
]

# Eliminar filas donde CUALQUIERA de las columnas especificadas tenga un valor nulo
# Esto se hace AHORA, para que el resto de la lógica opere sobre datos sin nulos
initial_rows = df.shape[0] # Para ver cuántas filas se eliminan
df.dropna(subset=columnas_a_verificar, inplace=True)
print(f"Filas eliminadas por nulos: {initial_rows - df.shape[0]}")
print(f"Filas restantes después de eliminar nulos: {df.shape[0]}")
# --- FIN DE NUEVA UBICACIÓN ---


# normalizar grupo (si esta columna también puede tener nulos o se maneja 'desconocido')
# Asegúrate de que 'grupo' no sea null antes de usar .str.lower().str.strip()
# o maneja los nulos en 'grupo' también si es necesario.
df['grupo'] = df['grupo'].astype(str).str.lower().str.strip() # Convertir a str antes de lower/strip


# dividir entre duplicados y no duplicados (AHORA ESTAS OPERANDO SOBRE UN DF SIN NULOS)
duplicados = df[df.duplicated(subset="id_unico", keep=False)]
no_duplicados = df[~df.duplicated(subset="id_unico", keep=False)]

# agrupar duplicados por id_unico
grupos = duplicados.groupby("id_unico")

# conservar solo los que tienen al menos un grupo válido
duplicados_limpios = grupos.filter(lambda g: (g["grupo"] != "desconocido").any())

# eliminar solo los que tienen grupo desconocido
duplicados_limpios = duplicados_limpios[duplicados_limpios["grupo"] != "desconocido"]

# ids que solo tienen "desconocido" y guardarlos aparte
ids_todos_desconocidos = grupos.filter(lambda g: (g["grupo"] == "desconocido").all())


# todo lo limpio
df_final = pd.concat([no_duplicados, duplicados_limpios], ignore_index=True)


# resultados
df_final.to_excel("TablasActuales/Tabla_estudiantes_7moa9no_limpia.xlsx", index=False)
ids_todos_desconocidos.to_excel("Segregaciones/Estudiantes_solo_desconocidos.xlsx", index=False)


# cuantas celdas tienen valor "desconocido"?
# Esta cantidad ahora se calculará sobre el 'df' que ya tiene las filas con nulos eliminadas.
cantidad = (df['grupo'] == 'desconocido').sum()

print("Limpieza completada.")
print(f"Estudiantes válidos guardados: {df_final.shape[0]}")
print(f"Estudiantes con solo datos 'desconocido' separados: {ids_todos_desconocidos.shape[0]}")
print(f'Cantidad de celdas con valor "desconocido": {cantidad}')