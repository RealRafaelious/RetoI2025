import pandas as pd

# Ruta
archivo = "C:/Users/Estudiante UCU/Repositorios/RetoI2025/Tabla_estudiantes_7moa9no.xlsx"

# Cargar
df = pd.read_excel(archivo)

# Dividir entre duplicados y no duplicados
duplicados = df[df.duplicated(subset="id_unico", keep=False)]
no_duplicados = df[~df.duplicated(subset="id_unico", keep=False)]

# Agrupar duplicados por id_unico
grupos = duplicados.groupby("id_unico")

# Filtrar duplicados: conservar solo los que tienen al menos un grupo válido
duplicados_limpios = grupos.filter(lambda g: (g["grupo"] != "desconocido").any())

# Dentro de esos grupos, eliminar solo los que tienen grupo desconocido
duplicados_limpios = duplicados_limpios[duplicados_limpios["grupo"] != "desconocido"]

# Detectar ids que solo tienen "desconocido" y guardarlos aparte
ids_todos_desconocidos = grupos.filter(lambda g: (g["grupo"] == "desconocido").all())

# Combinar todo lo limpio
df_final = pd.concat([no_duplicados, duplicados_limpios], ignore_index=True)

# Guardar resultados
df_final.to_excel("C:/Users/Estudiante UCU/Repositorios/RetoI2025/Tabla_estudiantes_7moa9no_limpia.xlsx", index=False)
ids_todos_desconocidos.to_excel("C:/Users/Estudiante UCU/Repositorios/RetoI2025/Estudiantes_solo_desconocidos.xlsx", index=False)

cantidad = (df['grupo'] == 'desconocido').sum()

print("Limpieza completada.")
print(f"Estudiantes válidos guardados: {df_final.shape[0]}")
print(f"Estudiantes con solo datos 'desconocido' separados: {ids_todos_desconocidos.shape[0]}")

print(f'Cantidad de celdas con valor "desconocido": {cantidad}')