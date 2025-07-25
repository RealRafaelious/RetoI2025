import pandas as pd

# 1. Cargar los tres archivos limpios
centros = pd.read_excel("Tabla_centros_7moa9no_limpia.xlsx")
docentes = pd.read_excel("Tabla_docentes_7moa9no_limpia.xlsx")
estudiantes = pd.read_excel("Tabla_estudiantes_7moa9no_limpia.xlsx")

# 2. Merge de docentes con centros (por id_centro)
docentes_centros = pd.merge(docentes, centros, on="id_centro", how="left")

# 3. Crear clave de unión en docentes y estudiantes
docentes_centros["clave_union"] = docentes_centros["id_centro"].astype(str) + "_" + docentes_centros["grado"].astype(str) + "_" + docentes_centros["grupo"].astype(str)
estudiantes["clave_union"] = estudiantes["id_centro"].astype(str) + "_" + estudiantes["grado"].astype(str) + "_" + estudiantes["grupo"].astype(str)

# 4. Merge final: estudiantes con docentes + centros (por clave_union)
final = pd.merge(estudiantes, docentes_centros, on="clave_union", how="left", suffixes=("_estudiante", "_docente"))

# 5. Guardar resultado
final.to_excel("Tabla_final_merge.xlsx", index=False)

print("✅ Merge completo. Archivo guardado como 'Tabla_final_merge.xlsx'")
