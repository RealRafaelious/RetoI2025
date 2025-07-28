import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os # Importar os para manejo de rutas



###############################################################################################
# 1. ¿Varía el uso de la plataforma CREA según el grado educativo? ¿Hay diferencias por sexo? #
###############################################################################################

# Detalles de estándares:
# Grado educativo: 7mo, 8vo, 9no
# Sexo: Masculino, Femenino
# Se tomaron en cuenta dentro de la muestra aquellas personas que se hayan conectado 10 o más veces.




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
    # Aquí podrías sys.exit(1) o simplemente dejar que el programa continúe con un df_estudiantes vacío
    # dependiendo de cómo quieras manejar este error. Por simplicidad, si no quieres salir abruptamente,
    # podrías asignar df_estudiantes = pd.DataFrame() y el resto del código manejará un DataFrame vacío.
    # Por ahora, simplemente saldré como se ha hecho en ejemplos anteriores si el archivo no existe.
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


# --- Aplicar el filtro de 30 o más conexiones en 'cr_total_dias_ingreso' ---
df_filtrado = df_estudiantes[df_estudiantes['cr_total_dias_ingreso'] >= 10].copy()

# Asegurarse de que las columnas 'grado' y 'sexo' estén limpias y sean consistentes
df_filtrado['grado'] = df_filtrado['grado'].astype(str).str.strip().str.lower()
df_filtrado['sexo'] = df_filtrado['sexo'].astype(str).str.strip().str.lower()


# Mapear grados a un orden específico para la visualización si son strings
# *** LA CORRECCIÓN CLAVE ES AQUÍ: '7', '8', '9' en lugar de '7mo', '8vo', '9no' ***
orden_grados = ['7', '8', '9']
# Filtra por grados que estén en tu orden_grados y asegúrate de que el 'grado' sea una categoría ordenada
df_filtrado = df_filtrado[df_filtrado['grado'].isin(orden_grados)].copy()

# Es vital verificar el df_filtrado AHORA
if df_filtrado.empty:
    print("\n¡Advertencia Crítica: df_filtrado está vacío DESPUÉS de filtrar por grados válidos!")
    print("Esto significa que no hay datos para los grados '7', '8', '9' con 30+ ingresos.")
    print("No se pueden generar gráficos ni estadísticas si el DataFrame está vacío.")
    import sys
    sys.exit(1) # Salir si el DataFrame está vacío después de este filtro crucial

df_filtrado['grado'] = pd.Categorical(df_filtrado['grado'], categories=orden_grados, ordered=True)

# Opcional: Mapear 'f'/'m' a 'femenino'/'masculino' para mejor visualización
# Si tus datos de sexo son 'F'/'M' y los quieres mostrar como 'Femenino'/'Masculino'
# Si no lo haces, se mostrarán 'f' y 'm' en las etiquetas del gráfico.
mapeo_sexo_display = {'f': 'femenino', 'm': 'masculino'}
df_filtrado['sexo_display'] = df_filtrado['sexo'].replace(mapeo_sexo_display)


print("Análisis de Uso de Plataforma CREA (con 10+ días de ingreso):\n")

# Uso promedio por grado educativo
# Añadir observed=True para silenciar FutureWarning si 'grado' es categórica
uso_por_grado = df_filtrado.groupby('grado', observed=True)['cr_total_dias_ingreso'].mean().reset_index()
print("Uso promedio por grado educativo:")
print(uso_por_grado)

# Uso promedio por sexo
# Usamos 'sexo' o 'sexo_display' para la agrupación
uso_por_sexo = df_filtrado.groupby('sexo', observed=True)['cr_total_dias_ingreso'].mean().reset_index()
print("\nUso promedio por sexo:")
print(uso_por_sexo)

# Uso promedio por grado y sexo
# Usamos 'sexo' o 'sexo_display' para la agrupación
uso_por_grado_sexo = df_filtrado.groupby(['grado', 'sexo'], observed=True)['cr_total_dias_ingreso'].mean().reset_index()
print("\nUso promedio por grado y sexo:")
print(uso_por_grado_sexo)


# --- Visualizaciones Gráficas ---

plt.style.use('seaborn-v0_8-darkgrid') # Estilo más estético

# Gráfico 1: Uso promedio por grado educativo
plt.figure(figsize=(8, 6))
# Añadir hue='grado' y legend=False para silenciar FutureWarning de palette
sns.barplot(x='grado', y='cr_total_dias_ingreso', data=uso_por_grado, hue='grado', legend=False, palette='viridis')
plt.title('Uso Promedio de CREA por Grado Educativo (Estudiantes con 10+ Ingresos)')
plt.xlabel('Grado Educativo')
plt.ylabel('Días Promedio de Ingreso a CREA')
plt.ylim(bottom=0) # Asegura que el eje y empiece en 0
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Gráfico 2: Uso promedio por sexo
plt.figure(figsize=(7, 5))
# Si usaste 'sexo_display', úsalo aquí. Si no, usa 'sexo'.
sns.barplot(x='sexo', y='cr_total_dias_ingreso', data=uso_por_sexo, hue='sexo', legend=False, palette='plasma')
plt.title('Uso Promedio de CREA por Sexo (Estudiantes con 10+ Ingresos)')
plt.xlabel('Sexo')
plt.ylabel('Días Promedio de Ingreso a CREA')
plt.ylim(bottom=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Gráfico 3: Uso promedio por grado y sexo
plt.figure(figsize=(10, 7))
# Si usaste 'sexo_display', úsalo aquí para el hue.
sns.barplot(x='grado', y='cr_total_dias_ingreso', hue='sexo', data=uso_por_grado_sexo, palette='coolwarm')
plt.title('Uso Promedio de CREA por Grado y Sexo (Estudiantes con 10+ Ingresos)')
plt.xlabel('Grado Educativo')
plt.ylabel('Días Promedio de Ingreso a CREA')
plt.ylim(bottom=0)
plt.legend(title='Sexo')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Gráfico 4: Distribución del uso de CREA por grado (Box Plot)
plt.figure(figsize=(10, 6))
sns.boxplot(x='grado', y='cr_total_dias_ingreso', data=df_filtrado, palette='cividis')
plt.title('Distribución del Uso de CREA por Grado Educativo (Estudiantes con 10+ Ingresos)')
plt.xlabel('Grado Educativo')
plt.ylabel('Días de Ingreso a CREA')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Gráfico 5: Distribución del uso de CREA por sexo (Box Plot)
plt.figure(figsize=(8, 6))
# Si usaste 'sexo_display', úsalo aquí.
sns.boxplot(x='sexo', y='cr_total_dias_ingreso', data=df_filtrado, palette='magma')
plt.title('Distribución del Uso de CREA por Sexo (Estudiantes con 10+ Ingresos)')
plt.xlabel('Sexo')
plt.ylabel('Días de Ingreso a CREA')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()