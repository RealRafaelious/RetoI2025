import pandas as pd

# Cargar el archivo
df = pd.read_excel("C:/Users/Estudiante UCU/Repositorios/RetoI2025/Tabla_estudiantes_7moa9no.xlsx")


# eliminar duplicados conservando la fila con más datos válidos
columnas_revisar = ["grupo"]

# columna auxiliar para contar cuántos campos NO son "desconocido"
df["valid_score"] = df[columnas_revisar].apply(lambda row: sum(x != "desconocido" and x != "sin datos" for x in row), axis=1)

# fila con más datos buenos arriba
df = df.sort_values(by=["id_unico", "valid_score"], ascending=[True, False])

# eliminar duplicados por id_unico, quedándose con la fila con más datos buenos
df = df.drop_duplicates(subset="id_unico", keep="first")

# borrar columna auxiliar
df = df.drop(columns=["valid_score"])

# Guardar el resultado limpio
df.to_excel("C:/Users/Estudiante UCU/Repositorios/RetoI2025/Tabla_estudiantes_7moa9no_limpia.xlsx", index=False)
print("Estudiantes limpios, duplicados eliminados.")
