import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Cargar archivo unido
df = pd.read_excel("TablasActuales/UNION.xlsx")

# Crear la nueva columna id_grupocentro combinando grupo_estudiante + id_centro_estudiante
df['id_grupocentro'] = df['grupo_estudiante'].astype(str) + df['id_centro_estudiante'].astype(str)

# Mostrar algunos ejemplos de la nueva columna
print("Ejemplos de la nueva columna id_grupocentro:")
print(df[['grupo_estudiante', 'id_centro_estudiante', 'id_grupocentro', 'grado_estudiante']].head(10))
print(f"\nTotal de combinaciones únicas grupo-centro: {df['id_grupocentro'].nunique()}")
print()

# Filtrar columnas necesarias y eliminar nulos
df_filtrado = df[["id_grupocentro", "dias_de_conexion_dispositivo", "grado_estudiante", "ivsmedia"]].dropna()

# Agrupar por grupo-centro
resumen = df_filtrado.groupby("id_grupocentro").agg(
    count=('dias_de_conexion_dispositivo', 'count'),
    mean=('dias_de_conexion_dispositivo', 'mean'),
    std=('dias_de_conexion_dispositivo', 'std'),
    grado=('grado_estudiante', 'first'),  # Tomar el primer valor de grado para cada grupo
    ivsmedia=('ivsmedia', 'first')  # Tomar el primer valor de ivsmedia para cada grupo
).reset_index()

# No calculamos CV - usamos directamente la desviación estándar
# La desviación estándar mide la variabilidad absoluta dentro de cada grupo
# Un valor bajo indica que los estudiantes del grupo tienen patrones similares

# Verificar los grados y quintiles disponibles
print("Grados disponibles en los datos:")
print(f"Grados únicos: {sorted(resumen['grado'].unique())}")
print(f"Conteo por grado en el resumen:")
print(resumen['grado'].value_counts().sort_index())
print()

print("Quintiles IVS disponibles en los datos:")
print(f"Quintiles únicos: {sorted(resumen['ivsmedia'].unique())}")
print(f"Conteo por quintil en el resumen:")
print(resumen['ivsmedia'].value_counts().sort_index())
print()

# INVESTIGACIÓN: Ver los grados en el dataset original
print("=== INVESTIGACIÓN DE GRADOS EN DATASET ORIGINAL ===")
print(f"Grados únicos en dataset original: {sorted(df['grado_estudiante'].unique())}")
print(f"Conteo de estudiantes por grado:")
print(df['grado_estudiante'].value_counts().sort_index())
print()

# Ver si hay problema con la agregación
print("=== VERIFICAR INTEGRIDAD DE DATOS ===")
print("Verificando si hay grupos mixtos (estudiantes de diferentes grados en el mismo grupo):")
verificacion_grupos = df.groupby('grupo_estudiante')['grado_estudiante'].agg(['nunique', 'min', 'max'])
grupos_mixtos = verificacion_grupos[verificacion_grupos['nunique'] > 1]
if len(grupos_mixtos) > 0:
    print(f"⚠️  PROBLEMA: Hay {len(grupos_mixtos)} grupos con estudiantes de múltiples grados!")
    print("Ejemplos de grupos mixtos:")
    print(grupos_mixtos.head(10))
    
    # Mostrar detalles de algunos grupos mixtos
    print("\nDetalles de grupos problemáticos:")
    for grupo in grupos_mixtos.head(5).index:
        estudiantes_grupo = df[df['grupo_estudiante'] == grupo]['grado_estudiante'].value_counts()
        print(f"  Grupo {grupo}: {dict(estudiantes_grupo)}")
else:
    print("✓ Todos los grupos tienen estudiantes del mismo grado")
print()

# Análisis detallado por grado
print("=== ANÁLISIS DETALLADO POR GRADO ===")
for grado in sorted(resumen['grado'].unique()):
    datos_grado = resumen[resumen['grado'] == grado]
    print(f"\nGRADO {grado}:")
    print(f"  • Número de grupos: {len(datos_grado)}")
    print(f"  • Promedio de conexión: {datos_grado['mean'].mean():.2f} días")
    print(f"  • Variabilidad promedio (std): {datos_grado['std'].mean():.2f}")
    print(f"  • Variabilidad mínima: {datos_grado['std'].min():.2f}")
    print(f"  • Variabilidad máxima: {datos_grado['std'].max():.2f}")
    print(f"  • Estudiantes promedio por grupo: {datos_grado['count'].mean():.1f}")

# Análisis detallado por quintil IVS
print("\n=== ANÁLISIS DETALLADO POR QUINTIL IVS ===")
for quintil in sorted(resumen['ivsmedia'].unique()):
    datos_quintil = resumen[resumen['ivsmedia'] == quintil]
    print(f"\n{quintil.upper()}:")
    print(f"  • Número de grupos: {len(datos_quintil)}")
    print(f"  • Promedio de conexión: {datos_quintil['mean'].mean():.2f} días")
    print(f"  • Variabilidad promedio (std): {datos_quintil['std'].mean():.2f}")
    print(f"  • Variabilidad mínima: {datos_quintil['std'].min():.2f}")
    print(f"  • Variabilidad máxima: {datos_quintil['std'].max():.2f}")
    print(f"  • Estudiantes promedio por grupo: {datos_quintil['count'].mean():.1f}")

# Comparación de variabilidad entre grados
print("\n=== COMPARACIÓN DE VARIABILIDAD POR GRADO ===")
variabilidad_por_grado = resumen.groupby('grado')['std'].agg(['mean', 'median', 'std']).round(2)
print("Estadísticas de variabilidad (desviación estándar) por grado:")
print(variabilidad_por_grado)

if 8 in variabilidad_por_grado.index and 7 in variabilidad_por_grado.index:
    std_grado8 = variabilidad_por_grado.loc[8, 'mean']
    std_grado7 = variabilidad_por_grado.loc[7, 'mean']
    if std_grado8 > std_grado7:
        diferencia = std_grado8 - std_grado7
        print(f"\n✓ CONFIRMADO: Grado 8 es más variable ({std_grado8:.2f}) que grado 7 ({std_grado7:.2f})")
        print(f"  Diferencia: {diferencia:.2f} puntos más de variabilidad")

# Comparación de variabilidad entre quintiles IVS
print("\n=== COMPARACIÓN DE VARIABILIDAD POR QUINTIL IVS ===")
variabilidad_por_quintil = resumen.groupby('ivsmedia')['std'].agg(['mean', 'median', 'std']).round(2)
print("Estadísticas de variabilidad (desviación estándar) por quintil IVS:")
print(variabilidad_por_quintil)
print()

# Definir colores específicos para cada quintil de ivsmedia
colores_quintiles = {
    'Quintil 1': '#B91C1C',      # Rojo oscuro - quintil más bajo
    'Quintil 2': '#F97316',      # Naranja - quintil bajo
    'Quintil 3': '#EAB308',      # Amarillo - quintil medio
    'Quintil 4': '#16A34A',      # Verde - quintil alto
    'Quintil 5': '#059669',      # Verde oscuro - quintil más alto
    'sin identificar': '#6B7280' # Gris - sin identificar
}

# Verificar que todos los quintiles tengan color asignado
quintiles_en_datos = set(resumen['ivsmedia'].unique())
quintiles_en_paleta = set(colores_quintiles.keys())
print(f"Quintiles en datos: {quintiles_en_datos}")
print(f"Quintiles en paleta: {quintiles_en_paleta}")
if not quintiles_en_datos.issubset(quintiles_en_paleta):
    print(f"Quintiles faltantes en paleta: {quintiles_en_datos - quintiles_en_paleta}")
print()

# Mostrar estadísticas descriptivas de la variabilidad por grupo
print("Estadísticas de la desviación estándar por grupo:")
print(f"Desv. estándar promedio: {resumen['std'].mean():.2f}")
print(f"Desv. estándar mediana: {resumen['std'].median():.2f}")
print(f"Desv. estándar mínima: {resumen['std'].min():.2f}")
print(f"Desv. estándar máxima: {resumen['std'].max():.2f}")
print("\nInterpretación:")
print("Std baja: Estudiantes con patrones de conexión similares")
print("Std alta: Estudiantes con patrones de conexión heterogéneos")

# Graficar scatterplot principal
plt.figure(figsize=(15, 10))

# Subplot 1: Scatterplot principal
plt.subplot(2, 2, 1)
sns.scatterplot(
    data=resumen,
    x='mean',
    y='std',
    size='count',
    hue='ivsmedia',  # Colorear por quintil de ivsmedia
    sizes=(10, 200),  # Tamaño mínimo y máximo de burbujas
    alpha=0.7,
    edgecolor='black',
    palette=colores_quintiles  # Usar colores específicos para cada quintil
)
plt.title("Variabilidad de uso de estudiantes por grupo-centro", fontsize=12)
plt.xlabel("Promedio de días de conexión")
plt.ylabel("Desviación estándar")
plt.grid(True, linestyle='--', alpha=0.5)

# Subplot 2: Distribución de variabilidad por quintil
plt.subplot(2, 2, 2)
for quintil in sorted(resumen['ivsmedia'].unique()):
    datos_quintil = resumen[resumen['ivsmedia'] == quintil]
    plt.hist(datos_quintil['std'], alpha=0.6, label=f'{quintil}', 
             color=colores_quintiles[quintil], bins=15)
plt.title("Distribución de Variabilidad por Quintil IVS", fontsize=12)
plt.xlabel("Desviación estándar")
plt.ylabel("Frecuencia")
plt.legend()
plt.grid(True, alpha=0.3)

# Subplot 3: Box plot de variabilidad por quintil
plt.subplot(2, 2, 3)
box_data = [resumen[resumen['ivsmedia'] == quintil]['std'] for quintil in sorted(resumen['ivsmedia'].unique())]
box_colors = [colores_quintiles[quintil] for quintil in sorted(resumen['ivsmedia'].unique())]
bp = plt.boxplot(box_data, labels=[f'{quintil}' for quintil in sorted(resumen['ivsmedia'].unique())], 
                 patch_artist=True)
for patch, color in zip(bp['boxes'], box_colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
plt.title("Variabilidad por Quintil IVS (Box Plot)", fontsize=12)
plt.ylabel("Desviación estándar")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

# Subplot 4: Número de grupos por quintil
plt.subplot(2, 2, 4)
grupos_por_quintil = resumen['ivsmedia'].value_counts().sort_index()
bars = plt.bar(range(len(grupos_por_quintil)), grupos_por_quintil.values, 
               color=[colores_quintiles[q] for q in grupos_por_quintil.index], alpha=0.7)
plt.title("Número de Grupos por Quintil IVS", fontsize=12)
plt.xlabel("Quintil IVS")
plt.ylabel("Número de grupos")
plt.xticks(range(len(grupos_por_quintil)), grupos_por_quintil.index, rotation=45)
plt.grid(True, alpha=0.3)
# Agregar valores en las barras
for bar, valor in zip(bars, grupos_por_quintil.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
             str(valor), ha='center', va='bottom')

plt.tight_layout()
plt.show()

