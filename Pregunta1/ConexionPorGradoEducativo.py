import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Define la ruta a tu archivo Excel
excel_estudiantes = "./TablasActuales/Tabla_estudiantes_7moa9no_limpia.xlsx"

try:
    df_estudiantes = pd.read_excel(excel_estudiantes)
    print(f"Archivo '{excel_estudiantes}' cargado exitosamente!")

except FileNotFoundError:
    print(f"Error: El archivo no fue encontrado en '{excel_estudiantes}'.")
    print("Por favor, verifica la ruta y el nombre del archivo, asegurándote de que sea correcto y accesible.")
    print("Directorio de trabajo actual:", os.getcwd())
    print("Ruta intentada (absoluta):", os.path.abspath(excel_estudiantes))
    sys.exit(1) # Sale del script con un código de error

except Exception as e:
    print(f"Ocurrió un error inesperado al intentar cargar '{excel_estudiantes}':")
    print(f"Detalles del error: {e}")
    sys.exit(1) # Sale del script

# Si el script llega hasta aquí, df_estudiantes debe estar definido
# Normaliza los nombres de las columnas
df_estudiantes.columns = [col.strip().lower().replace(" ", "_") for col in df_estudiantes.columns]
print("Nombres de columnas limpiados exitosamente.")
print("\nPrimeras 5 filas del DataFrame original después de limpiar nombres de columnas:")
print(df_estudiantes.head())

# --- INICIO DEPURACIÓN DE FILTROS (Estos prints fueron útiles, los mantengo como referencia pero pueden eliminarse más tarde) ---
print("\n--- INICIO DEPURACIÓN DE DATOS ---")

# 1. Inspecciona antes del filtro de 30+ conexiones
print("\nEstado del DataFrame ANTES de filtrar por 30+ conexiones:")
print("Dimensiones:", df_estudiantes.shape)
print("Estadísticas de 'cr_total_dias_ingreso':\n", df_estudiantes['cr_total_dias_ingreso'].describe())
print("Conteo de valores nulos en 'cr_total_dias_ingreso':", df_estudiantes['cr_total_dias_ingreso'].isnull().sum())
print("Valores únicos en 'cr_total_dias_ingreso' (primeros 10):", df_estudiantes['cr_total_dias_ingreso'].unique()[:10])


# Aplica el filtro de 30 o más conexiones en 'cr_total_dias_ingreso'
df_filtrado = df_estudiantes[df_estudiantes['cr_total_dias_ingreso'] >= 30].copy()

# 2. Inspecciona después del filtro de 30+ conexiones
print("\nEstado del DataFrame DESPUÉS de filtrar por 30+ conexiones:")
print("Dimensiones:", df_filtrado.shape)
if df_filtrado.empty:
    print("¡Advertencia: df_filtrado está vacío después del filtro de 30+ conexiones!")
else:
    print("Valores únicos de 'grado' antes de la normalización:", df_filtrado['grado'].unique())
    print("Valores únicos de 'sexo' antes de la normalización:", df_filtrado['sexo'].unique())


# Asegúrate de que las columnas 'grado' y 'sexo' estén limpias y sean consistentes
df_filtrado['grado'] = df_filtrado['grado'].astype(str).str.strip().str.lower()
df_filtrado['sexo'] = df_filtrado['sexo'].astype(str).str.strip().str.lower()

# 3. Inspecciona después de normalizar 'grado' y 'sexo'
print("\nEstado del DataFrame DESPUÉS de normalizar 'grado' y 'sexo':")
print("Dimensiones:", df_filtrado.shape)
if df_filtrado.empty:
    print("¡Advertencia: df_filtrado está vacío después de normalizar grado/sexo!")
else:
    print("Valores únicos de 'grado' normalizados:", df_filtrado['grado'].unique())
    print("Valores únicos de 'sexo' normalizados:", df_filtrado['sexo'].unique())


# Mapea grados a un orden específico para la visualización si son strings
# *** ¡ESTA FUE LA CORRECCIÓN CLAVE! ***
orden_grados = ['7', '8', '9'] # Corregido para que coincida con los valores reales de los datos ('7', '8', '9')
# Filtra por grados que estén en tu orden_grados y asegúrate de que 'grado' sea una categoría ordenada
df_filtrado = df_filtrado[df_filtrado['grado'].isin(orden_grados)].copy()

# 4. Inspecciona después del filtro por 'orden_grados'
print(f"\nEstado del DataFrame DESPUÉS de filtrar por grados válidos {orden_grados}:")
print("Dimensiones:", df_filtrado.shape)
if df_filtrado.empty:
    print(f"¡Advertencia: df_filtrado está vacío después de filtrar por grados en {orden_grados}!")
    print("Esta es la causa más probable de tus NaN y DataFrames vacíos.")
    sys.exit(1) # Sale si no hay datos para procesar después de este filtro crítico

df_filtrado['grado'] = pd.Categorical(df_filtrado['grado'], categories=orden_grados, ordered=True)

print("--- FIN DEPURACIÓN DE DATOS ---\n")
# --- FIN DEPURACIÓN DE FILTROS ---


print("Análisis de Uso de Plataforma CREA (con 30+ días de ingreso):\n")

# Añade observed=True a los groupbys para eliminar el FutureWarning
# Uso promedio por grado educativo
uso_por_grado = df_filtrado.groupby('grado', observed=True)['cr_total_dias_ingreso'].mean().reset_index()
print("Uso promedio por grado educativo:")
print(uso_por_grado)

# Uso promedio por sexo
uso_por_sexo = df_filtrado.groupby('sexo', observed=True)['cr_total_dias_ingreso'].mean().reset_index()
print("\nUso promedio por sexo:")
print(uso_por_sexo)

# Uso promedio por grado y sexo
uso_por_grado_sexo = df_filtrado.groupby(['grado', 'sexo'], observed=True)['cr_total_dias_ingreso'].mean().reset_index()
print("\nUso promedio por grado y sexo:")
print(uso_por_grado_sexo)

# --- Visualizaciones Gráficas ---

plt.style.use('seaborn-v0_8-darkgrid') # Estilo más estético

# Gráfico 1: Uso promedio por grado educativo
plt.figure(figsize=(8, 6))
# Añade hue='grado' y legend=False para silenciar FutureWarning de palette
sns.barplot(x='grado', y='cr_total_dias_ingreso', data=uso_por_grado, hue='grado', legend=False, palette='viridis')
plt.title('Uso Promedio de CREA por Grado Educativo (Estudiantes con 30+ Ingresos)')
plt.xlabel('Grado Educativo')
plt.ylabel('Días Promedio de Ingreso a CREA')
plt.ylim(bottom=0) # Asegura que el eje y empiece en 0
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Gráfico 2: Uso promedio por sexo
plt.figure(figsize=(7, 5))
# Añade hue='sexo' y legend=False para silenciar FutureWarning de palette
sns.barplot(x='sexo', y='cr_total_dias_ingreso', data=uso_por_sexo, hue='sexo', legend=False, palette='plasma')
plt.title('Uso Promedio de CREA por Sexo (Estudiantes con 30+ Ingresos)')
plt.xlabel('Sexo')
plt.ylabel('Días Promedio de Ingreso a CREA')
plt.ylim(bottom=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Gráfico 3: Uso promedio por grado y sexo (este ya tenía hue, está bien)
plt.figure(figsize=(10, 7))
sns.barplot(x='grado', y='cr_total_dias_ingreso', hue='sexo', data=uso_por_grado_sexo, palette='coolwarm')
plt.title('Uso Promedio de CREA por Grado y Sexo (Estudiantes con 30+ Ingresos)')
plt.xlabel('Grado Educativo')
plt.ylabel('Días Promedio de Ingreso a CREA')
plt.ylim(bottom=0)
plt.legend(title='Sexo')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Gráfico 4: Distribución del uso de CREA por grado (Box Plot)
plt.figure(figsize=(10, 6))
sns.boxplot(x='grado', y='cr_total_dias_ingreso', data=df_filtrado, palette='cividis')
plt.title('Distribución del Uso de CREA por Grado Educativo (Estudiantes con 30+ Ingresos)')
plt.xlabel('Grado Educativo')
plt.ylabel('Días de Ingreso a CREA')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Gráfico 5: Distribución del uso de CREA por sexo (Box Plot)
plt.figure(figsize=(8, 6))
sns.boxplot(x='sexo', y='cr_total_dias_ingreso', data=df_filtrado, palette='magma')
plt.title('Distribución del Uso de CREA por Sexo (Estudiantes con 30+ Ingresos)')
plt.xlabel('Sexo')
plt.ylabel('Días de Ingreso a CREA')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()