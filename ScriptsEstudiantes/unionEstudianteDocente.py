import pandas as pd
import re

# Ruta base
ruta = "TablasActuales/"

# Funciones de limpieza
def limpiar_grado(valor):
    match = re.search(r"[7-9]", str(valor))
    return match.group(0) if match else str(valor).strip().lower()

def limpiar_grupo(valor):
    match = re.search(r"[a-z]", str(valor).lower())
    return match.group(0) if match else str(valor).strip().lower()

def normalizar_columnas(df):
    df["id_centro"] = df["id_centro"].astype(str).str.strip()
    df["grado"] = df["grado"].apply(limpiar_grado)
    df["grupo"] = df["grupo"].apply(limpiar_grupo)
    return df

# Cargar archivos
centros = pd.read_excel(ruta + "Tabla_centros_7moa9no_limpia.xlsx")
docentes = pd.read_excel(ruta + "Tabla_docentes_7moa9no_limpia.xlsx")
estudiantes = pd.read_excel(ruta + "Tabla_estudiantes_7moa9no_limpia.xlsx")

# Normalizar columnas
centros["id_centro"] = centros["id_centro"].astype(str).str.strip()
docentes = normalizar_columnas(docentes)
estudiantes = normalizar_columnas(estudiantes)

# Crear clave_union
docentes["clave_union"] = docentes["id_centro"] + "_" + docentes["grado"] + "_" + docentes["grupo"]
estudiantes["clave_union"] = estudiantes["id_centro"] + "_" + estudiantes["grado"] + "_" + estudiantes["grupo"]

# Reducir docentes a uno por grupo
docentes_unicos = docentes.groupby("clave_union").first().reset_index()

# Agregar datos del centro
docentes_unicos = pd.merge(docentes_unicos, centros, on="id_centro", how="left")

# Merge final
final = pd.merge(estudiantes, docentes_unicos, on="clave_union", how="inner", suffixes=("_estudiante", "_docente"))

# Guardar resultado
final.to_excel(ruta + "UNION.xlsx", index=False)

print(f"✅ Archivo generado con {len(final)} estudiantes con docente asignado.")
print("📁 Guardado como TablasActuales/UNION.xlsx")