import pandas as pd

archivo = "C:/Users/Estudiante UCU/Repositorios/RetoI2025/Tabla_estudiantes_7moa9no.xlsx"
df = pd.read_excel(archivo)

# Normalizar nombres de columnas
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Limpiar columna 'grupo': eliminar espacios y pasar todo a minúsculas
df["grupo"] = df["grupo"].astype(str).str.strip().str.lower()

# Ver qué valores únicos hay en la columna 'grupo'
print("Valores únicos en grupo:", df["grupo"].unique())

# Buscar los ids que tienen al menos un grupo válido
ids_con_grupo_valido = df[df["grupo"] != "desconocido"]["id_unico"].unique()

# Eliminar filas con grupo 'desconocido' si ese id tiene otro grupo válido
condicion = (df["grupo"] == "desconocido") & (df["id_unico"].isin(ids_con_grupo_valido))
df_filtrado = df[~condicion]

# Guardar eliminados por si querés revisar
df[condicion].to_excel("C:/Users/Estudiante UCU/Repositorios/RetoI2025/Desconocidos_eliminados.xlsx", index=False)

# Guardar limpio
df_filtrado.to_excel("C:/Users/Estudiante UCU/Repositorios/RetoI2025/Tabla_estudiantes_7moa9no_limpia.xlsx", index=False)

# Reporte
print(f"Filas originales: {df.shape[0]}")
print(f"Filas eliminadas: {df.shape[0] - df_filtrado.shape[0]}")
print(f"Filas finales: {df_filtrado.shape[0]}")
