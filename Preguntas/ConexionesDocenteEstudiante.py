#################################################################################
# 3. ¿Los estudiantes que comparten docente muestran patrones de uso similares? #
#################################################################################

import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway, kruskal # Para comparar grupos (ANOVA o Kruskal-Wallis)

# --- Configuración de rutas (ajusta según tu estructura real) ---
# Esto asume que el script se encuentra en 'RETO1/RetoI2025/Preguntas'
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, '..') # Sube un nivel de 'Preguntas' a 'RetoI2025'

# Rutas a las tablas limpias (asegúrate de que estas rutas sean correctas)
ruta_estudiantes_limpia = os.path.join(project_root, "TablasActuales", "Tabla_estudiantes_7moa9no_limpia.xlsx")
# Asumo que tienes una tabla de docentes limpia, o que vas a usar "docente con materia"
# Necesitas una tabla que relacione docentes con los grupos/centros/materias que imparten.
# Si tu tabla de docentes es solo "docentes", no tendremos la información de grupo/materia.
# Si "docente con materia" es el archivo que tienes, ajusta la ruta.
ruta_docentes_con_materia = os.path.join(project_root, "TablasIniciales", "docente_con_materia.xlsx") # ¡Ajusta este nombre de archivo si es diferente!

# --- Función para cargar datos de forma segura ---
def cargar_datos(ruta_archivo, nombre_df):
    try:
        df = pd.read_excel(ruta_archivo)
        # Normalizar columnas al cargar para asegurar consistencia
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
        print(f"'{nombre_df}' cargado exitosamente desde '{ruta_archivo}' con {df.shape[0]} filas.")
        return df
    except FileNotFoundError:
        print(f"Error: El archivo '{ruta_archivo}' no fue encontrado para '{nombre_df}'.")
        sys.exit(1)
    except Exception as e:
        print(f"Error al cargar '{nombre_df}' desde '{ruta_archivo}': {e}")
        sys.exit(1)

# --- Cargar los DataFrames necesarios ---
df_estudiantes = cargar_datos(ruta_estudiantes_limpia, "Estudiantes Limpia")
df_docentes_materia = cargar_datos(ruta_docentes_con_materia, "Docentes con Materia")

# --- Paso 1: Entender cómo vincular estudiantes y docentes ---
# El vínculo más lógico es por id_centro, grado, ciclo y grupo.
# Asumimos que los docentes enseñan en ciertos id_centro, grado, ciclo y grupo.
# Y que los estudiantes pertenecen a un id_centro, grado, ciclo y grupo.

# Renombrar 'id_unico' en df_docentes_materia para evitar conflicto con id_unico de estudiantes
df_docentes_materia = df_docentes_materia.rename(columns={'id_unico': 'id_unico_docente'})

# Columnas clave para el merge
# Asegúrate de que estas columnas existan y sean consistentes en ambos DFs
columnas_vinculo = ['id_centro', 'grado', 'ciclo', 'grupo']

# Convertir columnas de vínculo a string para asegurar merges correctos (manejo de tipos mixtos)
for col in columnas_vinculo:
    if col in df_estudiantes.columns:
        df_estudiantes[col] = df_estudiantes[col].astype(str).str.strip().str.lower()
    if col in df_docentes_materia.columns:
        df_docentes_materia[col] = df_docentes_materia[col].astype(str).str.strip().str.lower()


# Realizar un merge para conectar estudiantes con los docentes que comparten sus atributos
# Esto creará duplicados de estudiantes si tienen múltiples docentes en el mismo grupo/centro/grado/ciclo
df_estudiantes_con_docentes = pd.merge(
    df_estudiantes,
    df_docentes_materia,
    on=columnas_vinculo,
    how='inner', # Solo estudiantes y docentes que tienen una coincidencia en los vínculos
    suffixes=('_estudiante', '_docente')
)

print(f"\nDataFrame combinado de estudiantes y docentes: {df_estudiantes_con_docentes.shape[0]} filas.")
# print(df_estudiantes_con_docentes.head()) # Para depuración

if df_estudiantes_con_docentes.empty:
    print("No se encontraron estudiantes que compartan vínculos (id_centro, grado, ciclo, grupo) con los docentes.")
    print("Por favor, revisa las columnas de vínculo en tus archivos de entrada.")
    sys.exit(1)

# --- Paso 2: Agrupar estudiantes por docente compartido ---
# Ahora, para cada docente, queremos analizar el uso de los estudiantes que le corresponden.
# Eliminamos duplicados de estudiantes por docente para que cada par (estudiante, docente) sea único
# Esto es importante si un estudiante aparece varias veces con el mismo docente debido a múltiples materias, etc.
df_estudiantes_con_docentes_unique = df_estudiantes_con_docentes.drop_duplicates(
    subset=['id_unico_estudiante', 'id_unico_docente']
).copy()


# Queremos agrupar por id_unico_docente y luego ver el comportamiento de los estudiantes asociados a él.
# Pero antes, vamos a asegurarnos de que solo estamos analizando estudiantes con 30+ días de ingreso a CREA
# ya que tu análisis anterior usaba este filtro. Puedes ajustar esto.
df_filtrado_uso = df_estudiantes_con_docentes_unique[
    df_estudiantes_con_docentes_unique['cr_total_dias_ingreso_estudiante'] >= 30
].copy()

if df_filtrado_uso.empty:
    print("\nAdvertencia: No hay estudiantes con 30+ días de ingreso a CREA que compartan docente.")
    print("Ajustando filtro o la muestra es demasiado pequeña para el análisis.")
    sys.exit(1)


print(f"\nNúmero de estudiantes (únicos por docente) con 30+ días de uso: {df_filtrado_uso.shape[0]}")

# Calcular métricas de uso por docente
# Nos interesan las columnas de uso de CREA y Dispositivo
metricas_uso = ['cr_total_dias_ingreso_estudiante', 'dias_de_conexion_dispositivo_estudiante']

# Agrupar por docente y calcular el promedio y desviación estándar de las métricas de uso para sus estudiantes
uso_por_docente = df_filtrado_uso.groupby('id_unico_docente')[metricas_uso].agg(['mean', 'std', 'count']).reset_index()
print("\nEstadísticas de uso de estudiantes agrupadas por docente:")
print(uso_por_docente.head())

# Filtrar docentes con un número mínimo de estudiantes para un análisis significativo
min_estudiantes_por_docente = 5 # Ajusta este umbral
docentes_significativos = uso_por_docente[uso_por_docente[('cr_total_dias_ingreso_estudiante', 'count')] >= min_estudiantes_por_docente]

if docentes_significativos.empty:
    print(f"\nNo hay docentes con al menos {min_estudiantes_por_docente} estudiantes válidos para el análisis. Reduce el umbral o revisa tus datos.")
    sys.exit(1)

print(f"\nDocentes con al menos {min_estudiantes_por_docente} estudiantes para análisis: {docentes_significativos.shape[0]}")

# --- Paso 3: Analizar patrones de uso y similaridad ---

print("\n--- Análisis de Similitud de Patrones de Uso por Docente ---")

# Idea: Visualizar la distribución de uso para los estudiantes de cada docente
# Limitaremos a los top N docentes con más estudiantes para visualización, si hay muchos
top_docentes_ids = docentes_significativos.sort_values(
    by=('cr_total_dias_ingreso_estudiante', 'count'), ascending=False
)['id_unico_docente'].head(5).tolist() # Top 5 docentes

plt.style.use('seaborn-v0_8-darkgrid')

# Gráfico de barras de promedio de uso de CREA por docente
plt.figure(figsize=(12, 7))
sns.barplot(
    x=docentes_significativos['id_unico_docente'].astype(str),
    y=docentes_significativos[('cr_total_dias_ingreso_estudiante', 'mean')],
    color='skyblue'
)
plt.errorbar(
    x=docentes_significativos['id_unico_docente'].astype(str),
    y=docentes_significativos[('cr_total_dias_ingreso_estudiante', 'mean')],
    yerr=docentes_significativos[('cr_total_dias_ingreso_estudiante', 'std')],
    fmt='none', capsize=5, color='black'
)
plt.title('Promedio de Días de Ingreso a CREA por Docente (con desviación estándar)')
plt.xlabel('ID del Docente')
plt.ylabel('Días Promedio de Ingreso a CREA')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Box plots para distribuciones de uso por docente (solo para el top N)
for metric in metricas_uso:
    plt.figure(figsize=(12, 7))
    sns.boxplot(
        x='id_unico_docente',
        y=metric,
        data=df_filtrado_uso[df_filtrado_uso['id_unico_docente'].isin(top_docentes_ids)],
        palette='viridis'
    )
    plt.title(f'Distribución de {metric} por Docente (Top {len(top_docentes_ids)} Docentes)')
    plt.xlabel('ID del Docente')
    plt.ylabel(metric.replace('_estudiante', ''))
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# --- Pruebas estadísticas para la similitud ---
print("\n--- Pruebas Estadísticas de Similitud de Uso ---")

# Vamos a realizar una prueba de ANOVA o Kruskal-Wallis para ver si los promedios/medianas
# de uso de CREA son significativamente diferentes entre los grupos de estudiantes de diferentes docentes.
# ANOVA: asume normalidad y homocedasticidad (varianzas iguales).
# Kruskal-Wallis: no asume normalidad ni homocedasticidad, es una alternativa no paramétrica.
# Dada la naturaleza de los "días de ingreso", Kruskal-Wallis suele ser más robusta.

for metric in metricas_uso:
    grupos_uso = [df_filtrado_uso[df_filtrado_uso['id_unico_docente'] == doc_id][metric].dropna()
                  for doc_id in docentes_significativos['id_unico_docente'].tolist()]
    
    # Filtrar grupos vacíos (docentes que no tienen estudiantes con datos para la métrica)
    grupos_uso = [g for g in grupos_uso if not g.empty]

    if len(grupos_uso) < 2:
        print(f"No hay suficientes grupos de docentes para realizar la prueba estadística para '{metric}'.")
        continue

    try:
        # Prueba de Kruskal-Wallis (no paramétrica)
        stat, p_value = kruskal(*grupos_uso)
        print(f"\nResultados de la prueba de Kruskal-Wallis para '{metric}':")
        print(f"Estadístico H: {stat:.3f}")
        print(f"P-valor: {p_value:.3e}")

        if p_value < 0.05:
            print("Conclusión: Hay una diferencia estadísticamente significativa en el uso entre los grupos de estudiantes de diferentes docentes.")
            print("Esto sugiere que el docente sí está relacionado con patrones de uso distintos.")
        else:
            print("Conclusión: No hay evidencia estadística suficiente para afirmar una diferencia en el uso entre los grupos de estudiantes de diferentes docentes.")
            print("Esto sugiere que los patrones de uso son similares o las diferencias son por azar.")
    except ValueError as ve:
        print(f"No se pudo realizar la prueba de Kruskal-Wallis para '{metric}': {ve}")
        print("Asegúrate de que cada grupo tenga al menos 5 observaciones no nulas.")

print("\n--- Análisis Finalizado ---")