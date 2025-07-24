import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# ruta
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
df_estudiantes.columns = [col.strip().lower().replace(" ", "_") for col in df_estudiantes.columns]
print("Nombres de columnas limpiados exitosamente.")

# ... el resto de tu código que usa df_estudiantes ...
print("\nPrimeras 5 filas del DataFrame:")
print(df_estudiantes.head())

    
    
# normalizar nombres de columnas
df_estudiantes.columns = [col.strip().lower().replace(" ", "_") for col in df_estudiantes.columns]

###############################################################################################
# 1. ¿Varía el uso de la plataforma CREA según el grado educativo? ¿Hay diferencias por sexo? #
###############################################################################################

# Detalles de estándares:
# Grado educativo: 7mo, 8vo, 9no
# Sexo: Masculino, Femenino
# Se tomaron en cuenta dentro de la muestra aquellas personas que se hayan conectado 30 o más veces.

# --- Aplicar el filtro de 30 o más conexiones en 'cr_total_dias_ingreso' ---
df_filtrado = df_estudiantes[df_estudiantes['cr_total_dias_ingreso'] >= 30].copy()

# Asegurarse de que las columnas 'grado' y 'sexo' estén limpias y sean consistentes
# (Esto es una buena práctica, asumiendo que ya tienes estos datos en buen estado,
# pero si no, podrías necesitar normalizarlos aquí también, similar a 'grupo' en tu otro script)
df_filtrado['grado'] = df_filtrado['grado'].astype(str).str.strip().str.lower()
df_filtrado['sexo'] = df_filtrado['sexo'].astype(str).str.strip().str.lower()

# Mapear grados a un orden específico para la visualización si son strings
# Puedes ajustar esto según cómo estén los grados en tus datos (ej. '7', '8', '9' o '7mo', '8vo', '9no')
orden_grados = ['7mo', '8vo', '9no']
# Filtra por grados que estén en tu orden_grados y asegúrate de que el 'grado' sea una categoría ordenada
df_filtrado = df_filtrado[df_filtrado['grado'].isin(orden_grados)].copy()
df_filtrado['grado'] = pd.Categorical(df_filtrado['grado'], categories=orden_grados, ordered=True)


print("Análisis de Uso de Plataforma CREA (con 30+ días de ingreso):\n")

# Uso promedio por grado educativo
uso_por_grado = df_filtrado.groupby('grado')['cr_total_dias_ingreso'].mean().reset_index()
print("Uso promedio por grado educativo:")
print(uso_por_grado)

# Uso promedio por sexo
uso_por_sexo = df_filtrado.groupby('sexo')['cr_total_dias_ingreso'].mean().reset_index()
print("\nUso promedio por sexo:")
print(uso_por_sexo)

# Uso promedio por grado y sexo
uso_por_grado_sexo = df_filtrado.groupby(['grado', 'sexo'])['cr_total_dias_ingreso'].mean().reset_index()
print("\nUso promedio por grado y sexo:")
print(uso_por_grado_sexo)

# --- Visualizaciones Gráficas ---

plt.style.use('seaborn-v0_8-darkgrid') # Estilo más estético

# Gráfico 1: Uso promedio por grado educativo
plt.figure(figsize=(8, 6))
sns.barplot(x='grado', y='cr_total_dias_ingreso', data=uso_por_grado, palette='viridis')
plt.title('Uso Promedio de CREA por Grado Educativo (Estudiantes con 30+ Ingresos)')
plt.xlabel('Grado Educativo')
plt.ylabel('Días Promedio de Ingreso a CREA')
plt.ylim(bottom=0) # Asegura que el eje y empiece en 0
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Gráfico 2: Uso promedio por sexo
plt.figure(figsize=(7, 5))
sns.barplot(x='sexo', y='cr_total_dias_ingreso', data=uso_por_sexo, palette='plasma')
plt.title('Uso Promedio de CREA por Sexo (Estudiantes con 30+ Ingresos)')
plt.xlabel('Sexo')
plt.ylabel('Días Promedio de Ingreso a CREA')
plt.ylim(bottom=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Gráfico 3: Uso promedio por grado y sexo
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