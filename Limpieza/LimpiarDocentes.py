import pandas as pd

# ruta
archivo = "TablasIniciales/Tabla_docentes_7moa9no.xlsx"

# cargar
df = pd.read_excel(archivo)

# noromalizar nombres de columnas
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]


# dividir entre duplicados y no duplicados
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

edad_promedio = df['edad'].mean()
df['edad'] = edad_promedio
print(f"Edad promedio de docentes: {edad_promedio:.2f}")
print("Edad de todos los docentes actualizada al promedio.")

# todo lo limpio
df_final = pd.concat([no_duplicados, duplicados_limpios], ignore_index=True)

# resultados
df_final.to_excel("TablasActuales/Tabla_docentes_7moa9no.xlsx", index=False)
ids_todos_desconocidos.to_excel("Segregaciones/Docentes_solo_desconocidos.xlsx", index=False)

# cuantas celdas tienen valor "desconocido"?
cantidad = (df['grupo'] == 'desconocido').sum()

print("Limpieza completada.")
print(f"Docentes válidos guardados: {df_final.shape[0]}")
print(f"Docentes con solo datos 'desconocido' separados: {ids_todos_desconocidos.shape[0]}")
print(f'Cantidad de celdas con valor "desconocido": {cantidad}')
