import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

###############################################################################################
# 1. ¿Varía el uso de la plataforma CREA según el grado educativo? ¿Hay diferencias por sexo? #
###############################################################################################

# Detalles de estándares:
# Grado educativo: 7mo, 8vo, 9no
# Sexo: Masculino, Femenino
# Se tomaron en cuenta dentro de la muestra aquellas personas que se hayan conectado 10 o más veces.

# --- Configuración de colores personalizados ---
# Define tu paleta de colores personalizada
colores_sexo = {
    'm': 'skyblue',  # Azul claro para masculino (si 'sexo' es 'm')
    'f': 'lightcoral' # Rosa claro para femenino (si 'sexo' es 'f')
    # Si usas 'sexo_display', sería:
    # 'masculino': 'skyblue',
    # 'femenino': 'lightcoral'
}

# Puedes ajustar la tonalidad de los colores si deseas:
# 'skyblue' es un azul claro. 'blue' sería un azul más oscuro.
# 'lightcoral' es un rosa salmón claro. 'pink' o 'hotpink' serían rosas más vibrantes.


# ruta
excel_estudiantes = "./TablasActuales/Tabla_estudiantes_7moa9no_limpia.xlsx"

# Se recomienda incluir el bloque try-except para manejar errores de carga del archivo
try:
    df_estudiantes = pd.read_excel(excel_estudiantes)
    print(f"Archivo '{excel_estudiantes}' cargado exitosamente!")
except FileNotFoundError:
    print(f"Error: El archivo no fue encontrado en '{excel_estudiantes}'.")
    print("Por favor, verifica la ruta y el nombre del archivo, asegurándote de que sea correcto y accesible.")
    print("Directorio de trabajo actual:", os.getcwd())
    print("Ruta intentada (absoluta):", os.path.abspath(excel_estudiantes))
    import sys
    sys.exit(1)
except Exception as e:
    print(f"Ocurrió un error inesperado al intentar cargar '{excel_estudiantes}':")
    print(f"Detalles del error: {e}")
    import sys
    sys.exit(1)


# normalizar nombres de columnas
df_estudiantes.columns = [col.strip().lower().replace(" ", "_") for col in df_estudiantes.columns]
print("Nombres de columnas limpiados exitosamente.")
print("\nPrimeras 5 filas del DataFrame:")
print(df_estudiantes.head())


# --- Aplicar el filtro de 10 o más conexiones en 'cr_total_dias_ingreso' ---
# Nota: La instrucción original decía 30, pero el código lo cambió a 10. Mantengo 10.
df_filtrado = df_estudiantes[df_estudiantes['cr_total_dias_ingreso'] >= 10].copy()

# Asegurarse de que las columnas 'grado' y 'sexo' estén limpias y sean consistentes
df_filtrado['grado'] = df_filtrado['grado'].astype(str).str.strip().str.lower()
df_filtrado['sexo'] = df_filtrado['sexo'].astype(str).str.strip().str.lower()


# Mapear grados a un orden específico para la visualización
orden_grados = ['7', '8', '9']
df_filtrado = df_filtrado[df_filtrado['grado'].isin(orden_grados)].copy()

if df_filtrado.empty:
    print("\n¡Advertencia Crítica: df_filtrado está vacío DESPUÉS de filtrar por grados válidos!")
    print("Esto significa que no hay datos para los grados '7', '8', '9' con 10+ ingresos.")
    print("No se pueden generar gráficos ni estadísticas si el DataFrame está vacío.")
    import sys
    sys.exit(1)

df_filtrado['grado'] = pd.Categorical(df_filtrado['grado'], categories=orden_grados, ordered=True)

# Mapear 'f'/'m' a 'femenino'/'masculino' para mejor visualización y para la leyenda
mapeo_sexo_display = {'f': 'Femenino', 'm': 'Masculino'}
df_filtrado['sexo_display'] = df_filtrado['sexo'].replace(mapeo_sexo_display)

# --- Ajustar la paleta de colores para el mapeo_sexo_display si lo usas en el gráfico ---
# Si mapeaste 'f' y 'm' a 'Femenino' y 'Masculino' para la visualización,
# entonces tu diccionario de colores también debe usar esas etiquetas.
colores_sexo_display = {
    'Masculino': 'skyblue',
    'Femenino': 'lightcoral'
}


print("Análisis de Uso de Plataforma CREA (con 10+ días de ingreso):\n")

# Uso promedio por grado educativo
uso_por_grado = df_filtrado.groupby('grado', observed=True)['cr_total_dias_ingreso'].mean().reset_index()
print("Uso promedio por grado educativo:")
print(uso_por_grado)

# Uso promedio por sexo
# Usamos 'sexo_display' para la agrupación si quieres que la tabla también muestre los nombres completos
uso_por_sexo = df_filtrado.groupby('sexo_display', observed=True)['cr_total_dias_ingreso'].mean().reset_index()
print("\nUso promedio por sexo:")
print(uso_por_sexo)

# Uso promedio por grado y sexo
# Usamos 'sexo_display' para la agrupación
uso_por_grado_sexo = df_filtrado.groupby(['grado', 'sexo_display'], observed=True)['cr_total_dias_ingreso'].mean().reset_index()
print("\nUso promedio por grado y sexo:")
print(uso_por_grado_sexo)


# --- Visualizaciones Gráficas ---

plt.style.use('seaborn-v0_8-darkgrid') # Estilo más estético

# Gráfico 1: Uso promedio por grado educativo (sin cambios, ya que no usa 'sexo')
plt.figure(figsize=(8, 6))
sns.barplot(x='grado', y='cr_total_dias_ingreso', data=uso_por_grado, hue='grado', legend=False, palette='viridis')
plt.title('Uso Promedio de CREA por Grado Educativo (Estudiantes con 10+ Ingresos)')
plt.xlabel('Grado Educativo')
plt.ylabel('Días Promedio de Ingreso a CREA')
plt.ylim(bottom=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Gráfico 2: Uso promedio por sexo (APLICANDO PALETA PERSONALIZADA)
plt.figure(figsize=(7, 5))
sns.barplot(x='sexo_display', y='cr_total_dias_ingreso', data=uso_por_sexo,
            palette=colores_sexo_display) # <-- ¡Aquí se aplica!
plt.title('Uso Promedio de CREA por Sexo (Estudiantes con 10+ Ingresos)')
plt.xlabel('Sexo')
plt.ylabel('Días Promedio de Ingreso a CREA')
plt.ylim(bottom=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Gráfico 3: Uso promedio por grado y sexo (APLICANDO PALETA PERSONALIZADA)
plt.figure(figsize=(10, 7))
sns.barplot(x='grado', y='cr_total_dias_ingreso', hue='sexo_display', data=uso_por_grado_sexo,
            palette=colores_sexo_display) # <-- ¡Aquí se aplica!
plt.title('Uso Promedio de CREA por Grado y Sexo (Estudiantes con 10+ Ingresos)')
plt.xlabel('Grado Educativo')
plt.ylabel('Días Promedio de Ingreso a CREA')
plt.ylim(bottom=0)
plt.legend(title='Sexo')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Gráfico 4: Distribución del uso de CREA por grado (Box Plot) (sin cambios)
plt.figure(figsize=(10, 6))
sns.boxplot(x='grado', y='cr_total_dias_ingreso', data=df_filtrado, palette='cividis')
plt.title('Distribución del Uso de CREA por Grado Educativo (Estudiantes con 10+ Ingresos)')
plt.xlabel('Grado Educativo')
plt.ylabel('Días de Ingreso a CREA')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Gráfico 5: Distribución del uso de CREA por sexo (Box Plot) (APLICANDO PALETA PERSONALIZADA)
plt.figure(figsize=(8, 6))
sns.boxplot(x='sexo_display', y='cr_total_dias_ingreso', data=df_filtrado,
            palette=colores_sexo_display) # <-- ¡Aquí se aplica!
plt.title('Distribución del Uso de CREA por Sexo (Estudiantes con 10+ Ingresos)')
plt.xlabel('Sexo')
plt.ylabel('Días de Ingreso a CREA')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()