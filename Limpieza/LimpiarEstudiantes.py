import pandas as pd


# --- Función para formatear fechas de Excel a formato datetime ---
def formatear_fechas_excel(df):
    """
    Convierte columnas que parecen fechas de Excel (números) a formato datetime.
    Detecta columnas que contengan 'fecha' o 'conexion' en su nombre.
    """
    df_copy = df.copy() # Trabaja en una copia para evitar SettingWithCopyWarning
    print("\n--- Formateando fechas ---")
    for col in df_copy.columns:
        # Identificar posibles columnas de fecha por el nombre
        # Asegúrate de que los nombres de las columnas estén normalizados (minúsculas, sin espacios)
        # antes de llamar a esta función, para que la detección sea precisa.
        if ('fecha' in col or 'conexion' in col) and 'dias_de_conexion' not in col:
            # Intentar convertir solo si la columna tiene valores numéricos que puedan ser fechas de Excel
            if pd.api.types.is_numeric_dtype(df_copy[col]) or \
               (df_copy[col].apply(lambda x: isinstance(x, (int, float)) and not pd.isna(x)).all() and \
                df_copy[col].min() >= 1): # Pequeña validación extra para evitar convertir años o IDs
                try:
                    # Convertir número de serie de Excel a datetime
                    # Excel usa 1899-12-30 como día 0 para fechas
                    df_copy[col] = pd.to_datetime(df_copy[col], unit='D', origin='1899-12-30')
                    print(f"Columna '{col}' convertida a formato de fecha.")
                except Exception as e:
                    print(f"Advertencia: No se pudo convertir la columna '{col}' a fecha. Error: {e}")
            elif pd.api.types.is_datetime64_any_dtype(df_copy[col]):
                print(f"Columna '{col}' ya está en formato de fecha. No se requiere conversión.")
            else:
                # Opcional: Puedes quitar este print si no quieres ver mensajes para cada columna no-fecha
                 print(f"Columna '{col}' no parece ser un formato de fecha de Excel ni datetime. Se ignora.")
                
    print("--- Fin formateo de fechas ---\n")
    return df_copy



# ruta
archivo = "TablasIniciales/Tabla_estudiantes_7moa9no.xlsx"

# cargar
df = pd.read_excel(archivo)

# normalizar nombres de columnas
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]


# normalizar grupo (si esta columna también puede tener nulos o se maneja 'desconocido')
# Asegúrate de que 'grupo' no sea null antes de usar .str.lower().str.strip()
# o maneja los nulos en 'grupo' también si es necesario.
df['grupo'] = df['grupo'].astype(str).str.lower().str.strip() # Convertir a str antes de lower/strip
df = formatear_fechas_excel(df)


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