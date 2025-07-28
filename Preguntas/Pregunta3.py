import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

########################################################################################
# 3. ¿Hay diferencias de uso del dispositivo y de CREA por contextos de vulnerabilidad?#
########################################################################################

docentes_estudiantes = pd.read_excel("TablasActuales/UNION.xlsx")
# --- 2. Preparación de datos ---

# --- 2. Preparación de datos ---

# *** CAMBIO CRÍTICO AQUÍ ***
# Convertir 'ivsmedia' para extraer el número del quintil
# Primero, asegúrate de que sea un string para usar str.extract
docentes_estudiantes['ivsmedia_temp'] = docentes_estudiantes['ivsmedia'].astype(str)

# Extraer el número usando una expresión regular
# \d+ busca uno o más dígitos
docentes_estudiantes['ivsmedia_quintil_numerico'] = docentes_estudiantes['ivsmedia_temp'].str.extract(r'(\d+)').astype(float)

# Eliminar la columna temporal
docentes_estudiantes.drop(columns=['ivsmedia_temp'], inplace=True)

# Ahora, eliminamos las filas donde no se pudo extraer un número (quedará NaN)
initial_rows_after_extraction = docentes_estudiantes.shape[0]
docentes_estudiantes.dropna(subset=['ivsmedia_quintil_numerico'], inplace=True)
print(f"Filas eliminadas por nulos en 'ivsmedia_quintil_numerico' después de extracción: {initial_rows_after_extraction - docentes_estudiantes.shape[0]}")


# Verificar si el DataFrame está vacío después de limpiar 'ivsmedia_quintil_numerico'
if docentes_estudiantes.empty:
    print("ERROR: El DataFrame está vacío después de limpiar nulos en la columna de quintil numérico. No se puede continuar el análisis.")
    exit()

# *** USAMOS LA COLUMNA NUMÉRICA PARA DEFINIR EL NIVEL DE VULNERABILIDAD ***
# Define las etiquetas de forma explícita y asegúrate del orden.
# Asumiendo que Quintil 1 es el más vulnerable y Quintil 5 el menos vulnerable.
labels_vulnerabilidad_map = {
    1.0: 'Quintil 1 (Más Vulnerable)',
    2.0: 'Quintil 2',
    3.0: 'Quintil 3',
    4.0: 'Quintil 4',
    5.0: 'Quintil 5 (Menos Vulnerable)'
}

# Mapear los valores numéricos de ivsmedia a las etiquetas descriptivas
docentes_estudiantes['nivel_vulnerabilidad'] = docentes_estudiantes['ivsmedia_quintil_numerico'].map(labels_vulnerabilidad_map)

# Convertir a tipo categórico y establecer el orden
# Es importante asegurarse de que solo se usen las etiquetas que realmente existen en tus datos
# y que 'ivsmedia_quintil_numerico' es de tipo int o float para el 'in labels_vulnerabilidad_map'
valid_quintiles_in_data = sorted(docentes_estudiantes['ivsmedia_quintil_numerico'].unique())
existing_labels = [labels_vulnerabilidad_map[q] for q in valid_quintiles_in_data if q in labels_vulnerabilidad_map]

# Es crucial que las categorías estén en el orden deseado para los gráficos (más vulnerable a menos vulnerable)
# Si tus datos tienen quintiles del 1 al 5 y 1 es el más vulnerable, el orden numérico ya es el correcto.
# Si solo aparecen algunos quintiles en tus datos, ajusta 'categories' para que solo incluyan los existentes.
docentes_estudiantes['nivel_vulnerabilidad'] = pd.Categorical(
    docentes_estudiantes['nivel_vulnerabilidad'],
    categories=existing_labels, # Usa solo las etiquetas para los quintiles presentes en tus datos
    ordered=True
)

print("\n--- Estado de la columna 'nivel_vulnerabilidad' (categórica) ---")
print(docentes_estudiantes['nivel_vulnerabilidad'].value_counts(dropna=False).sort_index())
print(f"Tipo de 'nivel_vulnerabilidad': {docentes_estudiantes['nivel_vulnerabilidad'].dtype}")
print(f"Valores únicos numéricos de 'ivsmedia' encontrados: {docentes_estudiantes['ivsmedia_quintil_numerico'].unique()}")


# Convertir columnas de fecha a datetime (resto del código igual)
docentes_estudiantes['primera_conexion_crea'] = pd.to_datetime(docentes_estudiantes['primera_conexion_crea'], errors='coerce')
docentes_estudiantes['primera_conexion_dispositivo'] = pd.to_datetime(docentes_estudiantes['primera_conexion_dispositivo'], errors='coerce')

# Asegurarse de que estas columnas de uso sean numéricas
docentes_estudiantes['cr_total_dias_ingreso'] = pd.to_numeric(docentes_estudiantes['cr_total_dias_ingreso'], errors='coerce')
docentes_estudiantes['dias_de_conexion_dispositivo'] = pd.to_numeric(docentes_estudiantes['dias_de_conexion_dispositivo'], errors='coerce')


# --- 4. Visualización de diferencias (resto del código igual) ---

plt.style.use('seaborn-v0_8-darkgrid')

# --- Gráfico 1: Uso del Dispositivo (dias_de_conexion_dispositivo) por Nivel de Vulnerabilidad ---
plt.figure(figsize=(10, 6))
data_for_plot1 = docentes_estudiantes.dropna(subset=['dias_de_conexion_dispositivo', 'nivel_vulnerabilidad'])
if not data_for_plot1.empty:
    sns.boxplot(x='nivel_vulnerabilidad', y='dias_de_conexion_dispositivo', data=data_for_plot1, palette='viridis')
    plt.title('Días de Conexión del Dispositivo por Nivel de Vulnerabilidad')
    plt.xlabel('Nivel de Vulnerabilidad (Basado en IVSMedia - Quintiles)')
    plt.ylabel('Días de Conexión del Dispositivo')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
else:
    print("No hay datos suficientes para el Gráfico 1 (dias_de_conexion_dispositivo).")


# --- Gráfico 2: Uso de CREA (cr_total_dias_ingreso) por Nivel de Vulnerabilidad ---
plt.figure(figsize=(10, 6))
data_for_plot2 = docentes_estudiantes.dropna(subset=['cr_total_dias_ingreso', 'nivel_vulnerabilidad'])
if not data_for_plot2.empty:
    sns.boxplot(x='nivel_vulnerabilidad', y='cr_total_dias_ingreso', data=data_for_plot2, palette='plasma')
    plt.title('Días de Ingreso a CREA por Nivel de Vulnerabilidad')
    plt.xlabel('Nivel de Vulnerabilidad (Basado en IVSMedia - Quintiles)')
    plt.ylabel('Días de Ingreso a CREA')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
else:
    print("No hay datos suficientes para el Gráfico 2 (cr_total_dias_ingreso).")


# --- Gráfico 3 (Opcional): Frecuencia de Primera Conexión a CREA por Nivel de Vulnerabilidad y Sexo ---
plt.figure(figsize=(12, 7))
data_for_plot3 = docentes_estudiantes.dropna(subset=['primera_conexion_crea', 'nivel_vulnerabilidad'])
if not data_for_plot3.empty:
    if 'sexo_estudiante' in data_for_plot3.columns:
        sns.countplot(x='nivel_vulnerabilidad', hue='sexo_estudiante', data=data_for_plot3, palette='cividis')
        plt.legend(title='Sexo del Estudiante')
    else:
        sns.countplot(x='nivel_vulnerabilidad', data=data_for_plot3, palette='cividis')
        print("Advertencia: La columna 'sexo_estudiante' no se encontró para el Gráfico 3. Se generó sin distinción de sexo.")
    plt.title('Conteo de Estudiantes con Primera Conexión a CREA por Nivel de Vulnerabilidad y Sexo')
    plt.xlabel('Nivel de Vulnerabilidad (Basado en IVSMedia - Quintiles)')
    plt.ylabel('Número de Estudiantes')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
else:
    print("No hay datos suficientes para el Gráfico 3 (primera_conexion_crea).")


# --- Gráfico 4 (Opcional): Frecuencia de Primera Conexión a Dispositivo por Nivel de Vulnerabilidad y Sexo ---
plt.figure(figsize=(12, 7))
data_for_plot4 = docentes_estudiantes.dropna(subset=['primera_conexion_dispositivo', 'nivel_vulnerabilidad'])
if not data_for_plot4.empty:
    if 'sexo_estudiante' in data_for_plot4.columns:
        sns.countplot(x='nivel_vulnerabilidad', hue='sexo_estudiante', data=data_for_plot4, palette='magma')
        plt.legend(title='Sexo del Estudiante')
    else:
        sns.countplot(x='nivel_vulnerabilidad', data=data_for_plot4, palette='magma')
        print("Advertencia: La columna 'sexo_estudiante' no se encontró para el Gráfico 4. Se generó sin distinción de sexo.")
    plt.title('Conteo de Estudiantes con Primera Conexión a Dispositivo por Nivel de Vulnerabilidad y Sexo')
    plt.xlabel('Nivel de Vulnerabilidad (Basado en IVSMedia - Quintiles)')
    plt.ylabel('Número de Estudiantes')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
else:
    print("No hay datos suficientes para el Gráfico 4 (primera_conexion_dispositivo).")


print("\nAnálisis gráfico completado. Revisa las ventanas emergentes con los gráficos.")
print("Los gráficos de caja (boxplot) muestran la distribución de los días de conexión.")
print("La línea en el medio de la caja es la mediana.")
print("La caja representa el 50% central de los datos (rango intercuartílico).")
print("Los 'bigotes' extienden la distribución, y los puntos son valores atípicos.")