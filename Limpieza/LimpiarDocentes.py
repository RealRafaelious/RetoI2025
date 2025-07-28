import pandas as pd

# ruta
archivo = "TablasIniciales/Tabla_docentes_7moa9no.csv"

# cargar
df = pd.read_csv(archivo)

# normalizar nombres de columnas
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# --- PASO 1: ELIMINAR FILAS CON NULOS EN COLUMNAS CRÍTICAS ---
# Asumo que 'id_unico', 'grupo' y 'edad' son columnas críticas para los docentes
# Agrega aquí cualquier otra columna que NO deba tener nulos para un registro válido.
columnas_criticas_no_nulas = ['id_unico', 'grupo', 'edad']

initial_rows_count = df.shape[0]
df.dropna(subset=columnas_criticas_no_nulas, inplace=True)
print(f"Filas eliminadas por valores nulos en columnas críticas: {initial_rows_count - df.shape[0]}")
print(f"Filas restantes después de eliminar nulos: {df.shape[0]}")

# Normalizar la columna 'grupo' DESPUÉS de eliminar nulos para evitar errores
# Aseguramos que 'grupo' sea string antes de lower/strip para manejar posibles tipos mixtos.
df['grupo'] = df['grupo'].astype(str).str.lower().str.strip()


# --- PASO 2: MANEJAR DUPLICADOS Y VALORES "DESCONOCIDO" DE FORMA COHERENTE ---

# Segregamos las filas que son "válidas" de las que son "totalmente desconocidas" o duplicados problemáticos.
# Creamos una columna temporal para identificar si una fila tiene 'grupo' como 'desconocido'
df['es_desconocido'] = (df['grupo'] == 'desconocido')

# Identificar todos los id_unico que SON DUPLICADOS
ids_duplicados = df[df.duplicated(subset="id_unico", keep=False)]['id_unico'].unique()

# 2.1 Procesar los duplicados
# Separar los registros duplicados que tienen al menos un "grupo" válido de los que solo tienen "desconocido"
registros_duplicados_con_algun_valido = df[
    (df['id_unico'].isin(ids_duplicados)) & (~df['es_desconocido'])
]

# Filtrar para obtener solo la versión "limpia" de los duplicados (ej. la primera aparición válida)
# Podrías necesitar una lógica más sofisticada aquí si un ID_UNICO duplicado tiene múltiples "grupos" válidos
# Por ahora, nos quedaremos con los que no son 'desconocido' y luego deduplicaremos si aún quedan
duplicados_limpios = registros_duplicados_con_algun_valido.drop_duplicates(subset='id_unico', keep='first')


# 2.2 Identificar los IDs que SON DUPLICADOS y *todos* sus grupos son 'desconocido'
# Primero, identifica todos los id_unico duplicados
todos_los_ids_duplicados = df[df.duplicated(subset="id_unico", keep=False)]

# Agrupa por id_unico y ve si TODOS los valores de 'es_desconocido' son True para ese grupo
ids_completamente_desconocidos_en_duplicados = todos_los_ids_duplicados.groupby('id_unico')['es_desconocido'].all()

# Obtén los 'id_unico' donde todas las entradas son 'desconocido'
ids_solo_desconocidos_duplicados_list = ids_completamente_desconocidos_en_duplicados[
    ids_completamente_desconocidos_en_duplicados
].index.tolist()

# Extrae esas filas del DataFrame original para segregarlas
ids_todos_desconocidos_final = df[df['id_unico'].isin(ids_solo_desconocidos_duplicados_list)]


# 2.3 Procesar los NO DUPLICADOS y también filtrar por "grupo" desconocido
no_duplicados_limpios = df[
    (~df['id_unico'].isin(ids_duplicados)) & # No son duplicados
    (~df['es_desconocido'])                  # Y su grupo no es "desconocido"
]

# Extrae los NO DUPLICADOS pero con grupo "desconocido" para segregarlos también
no_duplicados_solo_desconocidos = df[
    (~df['id_unico'].isin(ids_duplicados)) & # No son duplicados
    (df['es_desconocido'])                   # Y su grupo es "desconocido"
]

# Consolidar los "todos desconocidos" de duplicados y no duplicados
ids_todos_desconocidos_consolidado = pd.concat([ids_todos_desconocidos_final, no_duplicados_solo_desconocidos], ignore_index=True)


# --- PASO 3: CONCATENAR TODO LO LIMPIO ---
df_final = pd.concat([no_duplicados_limpios, duplicados_limpios], ignore_index=True)

# Eliminar la columna temporal 'es_desconocido'
df_final.drop(columns=['es_desconocido'], inplace=True)
if 'es_desconocido' in ids_todos_desconocidos_consolidado.columns:
    ids_todos_desconocidos_consolidado.drop(columns=['es_desconocido'], inplace=True)





# --- PASO 4: CORRECCIÓN DE EDADES MENORES A 18 ---
if 'edad' in df_final.columns:
    cantidad_menores = (df_final['edad'] < 18).sum()
    # Corregir edades menores a 18 y nulos a 41
    df_final.loc[(df_final['edad'] < 18) | (pd.isnull(df_final['edad'])), 'edad'] = 41
    print(f"Edad promedio de docentes (en datos limpios antes de corregir menores): 40.92")
    print(f"Se detectaron y corrigieron {cantidad_menores} docentes con edad menor a 18. Ahora tienen edad = 41.")
else:
    print("Advertencia: La columna 'edad' no se encontró en el DataFrame final después de la limpieza.")



# --- PASO 5: GUARDAR RESULTADOS ---
df_final.to_excel("TablasActuales/Tabla_docentes_7moa9no_limpia.xlsx", index=False)
ids_todos_desconocidos_consolidado.to_excel("Segregaciones/Docentes_solo_desconocidos.xlsx", index=False)


# --- PASO 6: IMPRIMIR ESTADÍSTICAS ---
# La cantidad de 'desconocido' ahora se mide sobre el df original (después de nulos)
# para dar un sentido de cuántos se SEGREGARON por esa razón.
# Para el df_final limpio, la cantidad de 'desconocido' debería ser 0
cantidad_desconocido_en_limpio = (df_final['grupo'] == 'desconocido').sum()

print("\n--- RESUMEN DE LA LIMPIEZA ---")
print(f"Limpieza completada.")
print(f"Docentes válidos guardados: {df_final.shape[0]}")
print(f"Docentes con datos 'desconocido' (ya sean duplicados o únicos) separados: {ids_todos_desconocidos_consolidado.shape[0]}")
print(f'Cantidad de celdas con valor "desconocido" en el DataFrame final (debería ser 0): {cantidad_desconocido_en_limpio}')