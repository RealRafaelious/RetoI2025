import pandas as pd

# Cargar archivo
archivo = "/Tabla_estudiantes_7moa9no.xlsx"
df = pd.read_excel(archivo)

# Normalizar nombres de columnas
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Limpiar columna 'grupo'
df["grupo"] = df["grupo"].astype(str).str.strip().str.lower()

# Verificar valores únicos en grupo
print("Valores únicos en grupo:", df["grupo"].unique())

# --- FILTRO 1: eliminar 'desconocido' si ese id tiene otro grupo válido ---
ids_con_grupo_valido = df[df["grupo"] != "desconocido"]["id_unico"].unique()
cond1 = (df["grupo"] == "desconocido") & (df["id_unico"].isin(ids_con_grupo_valido))
df = df[~cond1]

# --- FILTRO 2: eliminar duplicados exactos de grupo = 'desconocido' con misma edad, sexo e id_centro ---
cond2 = df["grupo"] == "desconocido"
df_desconocidos = df[cond2]
df_otros = df[~cond2]

# Eliminar duplicados dentro de los 'desconocido'
df_desconocidos = df_desconocidos.drop_duplicates(subset=["id_unico", "edad", "sexo", "id_centro"], keep="first")

# Combinar todo de nuevo
df = pd.concat([df_otros, df_desconocidos], ignore_index=True)

# --- FILTRO 3: eliminar filas sin ninguna conexión ---
# Convertir columnas de fechas a string para evitar errores si hay NaT/NaN
df["primera_conexion_crea"] = df["primera_conexion_crea"].astype(str).str.strip()
df["primera_conexion_dispositivo"] = df["primera_conexion_dispositivo"].astype(str).str.strip()

cond3 = (df["primera_conexion_crea"] == "") & (df["primera_conexion_dispositivo"] == "")
df = df[~cond3]

# Guardar archivo limpio
df.to_excel("/Tabla_estudiantes_7moa9no_limpia.xlsx", index=False)

# Reporte
print(f"Filas finales luego de todos los filtros: {df.shape[0]}")
