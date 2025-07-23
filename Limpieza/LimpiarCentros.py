from queue import Full
import pandas as pd

# ruta
centrosxlsx = "c:\Users\arias\Desktop\RETO1\Reto 1 - Datos - Ceibal\Datos\Tabla_centros_7moa9no.xlsx"

# cargar
df = pd.read_excel(centrosxlsx)

# noromalizar nombres de columnas
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]


# dividir entre duplicados y no duplicados
duplicados = df[df.duplicated(subset="id_centro", keep=False)]
no_duplicados = df[~df.duplicated(subset="id_centro", keep=False)]

# agrupar duplicados por id_centro
grupos = duplicados.groupby("id_centro")

# conservar solo los que tienen media de lvsMedia existente
duplicados_limpios = grupos.filter(lambda g: (g["lvsMedia"] != "" and g["lvsMedia"] is not None ).any())

# eliminar solo los que tienen grupo desconocido
duplicados_limpios = duplicados_limpios[duplicados_limpios["lvsMedia"] !=  "" and g["lvsMedia"] is not None]

# ids que solo tienen "desconocido" y guardarlos aparte
ids_todos_desconocidos = grupos.filter(lambda g: (g["lvsMedia"] != "" and g["lvsMedia"] is not None ).all())

# todo lo limpio
df_final = pd.concat([no_duplicados, duplicados_limpios], ignore_index=True)

# resultados
df_final.to_excel("C:/Users/Estudiante UCU/Repositorios/RetoI2025/Tabla_estudiantes_7moa9no_limpia.xlsx", index=False)
ids_todos_desconocidos.to_excel("C:/Users/Estudiante UCU/Repositorios/RetoI2025/Estudiantes_solo_desconocidos.xlsx", index=False)

# cuantas celdas tienen valor "desconocido"?
cantidad = (df['grupo'] == 'desconocido').sum()

print("Limpieza completada.")
print(f"Estudiantes válidos guardados: {df_final.shape[0]}")
print(f"Estudiantes con solo datos 'desconocido' separados: {ids_todos_desconocidos.shape[0]}")
print(f'Cantidad de celdas con valor "desconocido": {cantidad}')
