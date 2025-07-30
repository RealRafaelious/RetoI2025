import pandas as pd

# Cargar los datos
df = pd.read_excel("TablasActuales/UNION.xlsx")

print("=== ANÁLISIS DE GRUPOS POR CENTRO Y GRADO ===\n")

# 1. Cuántos grupos hay de cada grado
print("1. GRUPOS POR GRADO:")
print("=" * 30)
grupos_por_grado = df.groupby('grado_estudiante')['Grupo'].nunique().sort_index()
print(grupos_por_grado)
print(f"\nTotal de grupos únicos: {df['Grupo'].nunique()}")
print()

# 2. Cuántos grupos hay en cada centro
print("2. GRUPOS POR CENTRO:")
print("=" * 30)
grupos_por_centro = df.groupby('id_centro_docente')['Grupo'].nunique().sort_values(ascending=False)
print(grupos_por_centro)
print()

# 3. Distribución detallada: grado por centro
print("3. DISTRIBUCIÓN DETALLADA (GRADO x CENTRO):")
print("=" * 50)
tabla_cruzada = pd.crosstab(df['grado_estudiante'], df['id_centro_docente'], 
                           values=df['Grupo'], aggfunc='nunique', fill_value=0)
print(tabla_cruzada)
print()

# 4. Resumen estadístico
print("4. RESUMEN ESTADÍSTICO:")
print("=" * 30)
print(f"• Total de centros: {df['id_centro_docente'].nunique()}")
print(f"• Total de grados: {df['grado_estudiante'].nunique()}")
print(f"• Total de grupos únicos: {df['Grupo'].nunique()}")
print(f"• Promedio de grupos por centro: {grupos_por_centro.mean():.1f}")
print(f"• Centro con más grupos: {grupos_por_centro.index[0]} ({grupos_por_centro.iloc[0]} grupos)")
print(f"• Centro con menos grupos: {grupos_por_centro.index[-1]} ({grupos_por_centro.iloc[-1]} grupos)")
print()

# 5. Verificar si hay grupos mixtos (estudiantes de diferentes grados)
print("5. VERIFICACIÓN DE GRUPOS MIXTOS:")
print("=" * 40)
grupos_mixtos = df.groupby('Grupo')['grado_estudiante'].nunique()
grupos_con_multiple_grado = grupos_mixtos[grupos_mixtos > 1]

if len(grupos_con_multiple_grado) > 0:
    print(f"¡ATENCIÓN! Hay {len(grupos_con_multiple_grado)} grupos con estudiantes de múltiples grados:")
    print(grupos_con_multiple_grado)
else:
    print("✓ Todos los grupos tienen estudiantes del mismo grado")
