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
                # print(f"Columna '{col}' no parece ser un formato de fecha de Excel ni datetime. Se ignora.")
                pass # No hacer nada si no es una columna de fecha potencial
    print("--- Fin formateo de fechas ---\n")
    return df_copy
