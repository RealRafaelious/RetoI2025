import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

########################################################################################
# 3. ¿Hay diferencias de uso del dispositivo y de CREA por contextos de vulnerabilidad?#
########################################################################################

docentes_estudiantes = pd.read_excel("TablasActuales/UNION.xlsx")
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

# *** CÁLCULO DE PORCENTAJES PARA LAS ETIQUETAS ***
# Calcular el conteo de cada quintil
quintil_counts = docentes_estudiantes['ivsmedia_quintil_numerico'].value_counts(normalize=False)
total_students = quintil_counts.sum()
quintil_percentages = (quintil_counts / total_students * 100).sort_index()

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
valid_quintiles_in_data = sorted(docentes_estudiantes['ivsmedia_quintil_numerico'].unique())
existing_labels = [labels_vulnerabilidad_map[q] for q in valid_quintiles_in_data if q in labels_vulnerabilidad_map]

# Crear las nuevas etiquetas incluyendo el porcentaje
new_x_labels = []
for q_num in sorted(valid_quintiles_in_data):
    if q_num in labels_vulnerabilidad_map:
        original_label = labels_vulnerabilidad_map[q_num]
        percentage = quintil_percentages.get(q_num, 0) # Usa .get para manejar si un quintil no tiene datos
        new_x_labels.append(f"{original_label}\n({percentage:.1f}%)") # Formato: "Quintil X (Descripción)\n(YY.Y%)"

# Asegúrate de que las categorías del DataFrame también incluyan los porcentajes si deseas que se usen directamente
# para el ordenamiento interno del boxplot/barplot, aunque normalmente con 'ordered=True' basta.
# Para el caso de las etiquetas del eje x, las estableceremos manualmente después de crear el gráfico.
docentes_estudiantes['nivel_vulnerabilidad'] = pd.Categorical(
    docentes_estudiantes['nivel_vulnerabilidad'],
    categories=existing_labels, # Aquí mantenemos las etiquetas originales para el orden categórico
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




# Preparar datos para gráfico combinado
df_crea = docentes_estudiantes[['nivel_vulnerabilidad', 'cr_total_dias_ingreso']].copy()
df_crea = df_crea.dropna()
df_crea['tipo_conexion'] = 'CREA'
df_crea.rename(columns={'cr_total_dias_ingreso': 'dias_conexion'}, inplace=True)

df_disp = docentes_estudiantes[['nivel_vulnerabilidad', 'dias_de_conexion_dispositivo']].copy()
df_disp = df_disp.dropna()
df_disp['tipo_conexion'] = 'Dispositivo'
df_disp.rename(columns={'dias_de_conexion_dispositivo': 'dias_conexion'}, inplace=True)

# Unir ambos para comparar
df_combined = pd.concat([df_crea, df_disp], axis=0)

# Gráfico combinado
plt.figure(figsize=(12, 7))
sns.boxplot(x='nivel_vulnerabilidad', y='dias_conexion', hue='tipo_conexion', data=df_combined, palette='Set2')
plt.title('Comparación de Días de Conexión por Nivel de Vulnerabilidad')
plt.xlabel('Nivel de Vulnerabilidad (IVSMedia - Quintiles)')
plt.ylabel('Días de Conexión')
plt.legend(title='Tipo de Conexión')
# Establecer las etiquetas del eje X con los porcentajes
plt.xticks(ticks=range(len(new_x_labels)), labels=new_x_labels, rotation=45, ha='right')
plt.tight_layout()
plt.show()


plt.figure(figsize=(12, 6))
sns.barplot(data=df_combined, x='nivel_vulnerabilidad', y='dias_conexion', hue='tipo_conexion', ci='sd', palette='Set2')
plt.title('Promedio de Días de Conexión por Quintil y Tipo de Conexión')
plt.ylabel('Días de Conexión Promedio')
plt.xlabel('Nivel de Vulnerabilidad')
plt.legend(title='Tipo de Conexión')
# Establecer las etiquetas del eje X con los porcentajes
plt.xticks(ticks=range(len(new_x_labels)), labels=new_x_labels, rotation=45, ha='right')
plt.tight_layout()
plt.show()


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
    # Establecer las etiquetas del eje X con los porcentajes
    plt.xticks(ticks=range(len(new_x_labels)), labels=new_x_labels, rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
else:
    print("No hay datos suficientes para el Gráfico 4 (primera_conexion_dispositivo).")


print("\nAnálisis gráfico completado. Revisa las ventanas emergentes con los gráficos.")
print("Los gráficos de caja (boxplot) muestran la distribución de los días de conexión.")
print("La línea en el medio de la caja es la mediana.")
print("La caja representa el 50% central de los datos (rango intercuartílico).")
print("Los 'bigotes' extienden la distribución, y los puntos son valores atípicos.")