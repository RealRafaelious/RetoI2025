import pandas as pd
import os
import sys

# --- Función para formatear fechas de Excel a formato datetime ---
def formatear_fechas_excel(df):
    """
    Convierte columnas que parecen fechas de Excel (números o strings) a formato datetime.
    Detecta columnas que contengan 'fecha' o 'conexion' en su nombre,
    excluyendo 'dias_de_conexion'.
    """
    df_copy = df.copy()
    print("\n--- Iniciando formateo de fechas ---")
    
    for col in df_copy.columns:
        col_lower = col.lower() 

        if ('fecha' in col_lower or 'conexion' in col_lower) and 'dias_de_conexion' not in col_lower:
            
            if pd.api.types.is_datetime64_any_dtype(df_copy[col]):
                print(f"Columna '{col}' ya está en formato de fecha. No se requiere conversión.")
                continue

            is_numeric_and_not_nan = df_copy[col].apply(lambda x: isinstance(x, (int, float)) and not pd.isna(x))
            
            if is_numeric_and_not_nan.any():
                try:
                    df_copy.loc[is_numeric_and_not_nan, col] = pd.to_datetime(
                        df_copy.loc[is_numeric_and_not_nan, col], unit='D', origin='1899-12-30', errors='coerce'
                    )
                    print(f"Columna '{col}' (numérica) convertida a formato de fecha.")
                except Exception as e:
                    print(f"Advertencia: No se pudo convertir la columna numérica '{col}' a fecha. Error: {e}")
            
            elif pd.api.types.is_object_dtype(df_copy[col]):
                original_dtype = df_copy[col].dtype
                df_copy[col] = pd.to_datetime(df_copy[col], errors='coerce')
                
                if df_copy[col].dtype == 'datetime64[ns]' and original_dtype != df_copy[col].dtype:
                    print(f"Columna '{col}' (string/objeto) convertida a formato de fecha.")
                else:
                    if not pd.api.types.is_datetime64_any_dtype(df_copy[col]):
                        print(f"Columna '{col}' (string/objeto) no parece ser un formato de fecha válido. Se ignora.")
            else:
                pass

    print("--- Fin formateo de fechas ---\n")
    return df_copy


# --- Rutas de archivos ---
# Determinar la ruta base del proyecto de forma más robusta
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, '..') 

excel_estudiantes_inicial = os.path.join(project_root, "TablasIniciales", "Tabla_estudiantes_7moa9no.xlsx")

excel_estudiantes_limpia = os.path.join(project_root, "TablasActuales", "Tabla_estudiantes_7moa9no_limpia.xlsx")
excel_segregados_desconocidos = os.path.join(project_root, "Segregaciones", "Estudiantes_solo_desconocidos.xlsx")


# --- Crear directorios de salida si no existen ---
os.makedirs(os.path.dirname(excel_estudiantes_limpia), exist_ok=True)
os.makedirs(os.path.dirname(excel_segregados_desconocidos), exist_ok=True)


# --- Cargar datos iniciales ---
try:
    df = pd.read_excel(excel_estudiantes_inicial)
    print(f"Archivo '{excel_estudiantes_inicial}' cargado exitosamente!")
except FileNotFoundError:
    print(f"Error: El archivo no fue encontrado en '{excel_estudiantes_inicial}'.")
    print("Por favor, verifica la ruta y el nombre del archivo, asegurándote de que sea correcto y accesible.")
    print("Directorio de trabajo actual:", os.getcwd())
    print("Ruta intentada (absoluta):", os.path.abspath(excel_estudiantes_inicial))
    sys.exit(1)
except Exception as e:
    print(f"Ocurrió un error inesperado al intentar cargar '{excel_estudiantes_inicial}':")
    print(f"Detalles del error: {e}")
    sys.exit(1)


# --- Normalizar nombres de columnas ---
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
print("Nombres de columnas limpiados exitosamente.")


# --- Normalizar columna 'grupo' ---
df['grupo'] = df['grupo'].astype(str).str.lower().str.strip()
print("Columna 'grupo' normalizada.")


# --- Formatear fechas ---
df = formatear_fechas_excel(df)


# --- INICIO DEL NUEVO CÓDIGO PARA FILTRAR POR DÍAS DE CONEXIÓN ---
initial_rows_before_connection_filter = df.shape[0]
print(f"\n--- Aplicando filtro: estudiantes con menos de 10 días de conexión ({'cr_total_dias_ingreso'}) serán eliminados ---")

# Asegurarse de que 'cr_total_dias_ingreso' sea numérico para el filtro
# Si hay nulos en esta columna, puedes decidir cómo manejarlos antes del filtro
# Por ejemplo, rellenarlos con 0 o eliminarlos si no quieres incluirlos en el conteo de días
if 'cr_total_dias_ingreso' in df.columns:
    # Convertir a numérico, coercing errores a NaN. Luego rellenar NaN con 0 para que no fallen el filtro
    df['cr_total_dias_ingreso'] = pd.to_numeric(df['cr_total_dias_ingreso'], errors='coerce').fillna(0)
    
    # Aplicar el filtro: conservar solo filas donde 'cr_total_dias_ingreso' es >= 10
    df = df[df['cr_total_dias_ingreso'] >= 10].copy()
    
    rows_after_connection_filter = df.shape[0]
    print(f"Filas eliminadas por menos de 10 días de conexión: {initial_rows_before_connection_filter - rows_after_connection_filter}")
    print(f"Filas restantes después del filtro de conexión: {rows_after_connection_filter}")
else:
    print(f"Advertencia: Columna 'cr_total_dias_ingreso' no encontrada. No se aplicó el filtro de conexión.")

print("--- Fin del filtro por días de conexión ---\n")
# --- FIN DEL NUEVO CÓDIGO ---


# --- INICIO DE LA SOLUCIÓN ALTERNATIVA PARA EL PROBLEMA DE datetime_format ---
# Convertir explícitamente las columnas de fecha a string ANTES de guardar
# Si tu Pandas no soporta datetime_format, esta es la forma de forzar la visualización en Excel
for col in ['primera_conexion_crea', 'primera_conexion_dispositivo']:
    if col in df.columns and pd.api.types.is_datetime64_any_dtype(df[col]):
        # Solo convierte a string si la columna es realmente de tipo datetime
        df[col] = df[col].dt.strftime('%Y-%m-%d') # Formato de fecha deseado como string
        print(f"Columna '{col}' formateada a string para exportación a Excel.")
# --- FIN DE LA SOLUCIÓN ALTERNATIVA ---


# --- Separar duplicados y no duplicados por 'id_unico' ---
duplicados = df[df.duplicated(subset="id_unico", keep=False)].copy() 
no_duplicados = df[~df.duplicated(subset="id_unico", keep=False)].copy()

# --- Procesar duplicados ---
if not duplicados.empty:
    grupos = duplicados.groupby("id_unico")

    duplicados_limpios = grupos.filter(lambda g: (g["grupo"] != "desconocido").any()).copy()
    duplicados_limpios = duplicados_limpios[duplicados_limpios["grupo"] != "desconocido"].copy()

    ids_todos_desconocidos = grupos.filter(lambda g: (g["grupo"] == "desconocido").all()).copy()
else:
    duplicados_limpios = pd.DataFrame(columns=df.columns) 
    ids_todos_desconocidos = pd.DataFrame(columns=df.columns)

# --- Concatenar todo lo limpio para el DataFrame final ---
df_final = pd.concat([no_duplicados, duplicados_limpios], ignore_index=True)


# --- Calcular cantidad de celdas con valor "desconocido" ---
# Esta cantidad se calcula sobre el 'df' después de la carga y el filtro de conexión
cantidad_desconocido = (df['grupo'] == 'desconocido').sum()


# --- Guardar resultados ---
try:
    # Ahora, ya no usamos datetime_format aquí, porque las columnas ya son strings
    df_final.to_excel(excel_estudiantes_limpia, index=False)
    print(f"Estudiantes válidos guardados en: '{excel_estudiantes_limpia}'")
    
    ids_todos_desconocidos.to_excel(excel_segregados_desconocidos, index=False)
    print(f"Estudiantes con solo datos 'desconocido' separados en: '{excel_segregados_desconocidos}'")

except Exception as e:
    print(f"Error al guardar los archivos Excel: {e}")


# --- Resumen final ---
print("\n--- Resumen de la Limpieza ---")
print(f"Limpieza completada.")
print(f"Estudiantes válidos guardados: {df_final.shape[0]}")
print(f"Estudiantes con solo datos 'desconocido' separados: {ids_todos_desconocidos.shape[0]}")
print(f'Cantidad total de celdas con valor "desconocido" (antes de la segregación final): {cantidad_desconocido}')
print("----------------------------")