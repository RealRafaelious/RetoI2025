import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Cargar archivo unido
df = pd.read_excel("TablasActuales/UNION.xlsx")

# Crear la nueva columna id_grupocentro combinando ciclo_docente + id_centro
df['id_grupocentro'] = df['ciclo_docente'].astype(str) + df['id_centro_docente'].astype(str)

# Mostrar algunos ejemplos de la nueva columna
print("Ejemplos de la nueva columna id_grupocentro:")
print(df[['ciclo_docente', 'id_centro_docente', 'id_grupocentro']].head(10))
print(f"\nTotal de combinaciones únicas grupo-centro: {df['id_grupocentro'].nunique()}")
print()

# Filtrar columnas necesarias y eliminar nulos
df_filtrado = df[["id_grupocentro", "dias_de_conexion_dispositivo", "ivsmedia"]].dropna()

# Agrupar por grupo-centro
resumen = df_filtrado.groupby("id_grupocentro").agg(
    count=('dias_de_conexion_dispositivo', 'count'),
    mean=('dias_de_conexion_dispositivo', 'mean'),
    std=('dias_de_conexion_dispositivo', 'std'),
    ivsmedia=('ivsmedia', 'first')  # Tomar el primer valor de ivsmedia para cada grupo
).reset_index()

# Calcular coeficiente de variación (CV = std/mean)
resumen['cv'] = resumen['std'] / resumen['mean']

# Verificar los quintiles disponibles
print("Quintiles disponibles en los datos:")
print(resumen['ivsmedia'].unique())
print()

# Definir colores específicos para cada quintil
colores_quintiles = {
    'Quintil 1': '#E74C3C',  # Rojo brillante
    'Quintil 2': '#F39C12',  # Naranja brillante
    'Quintil 3': '#F1C40F',  # Amarillo brillante
    'Quintil 4': '#27AE60',  # Verde brillante
    'Quintil 5': '#3498DB',  # Azul brillante
    'sin identificar': '#95A5A6'  # Gris claro para sin identificar
}

# Verificar que todos los quintiles tengan color asignado
quintiles_en_datos = set(resumen['ivsmedia'].unique())
quintiles_en_paleta = set(colores_quintiles.keys())
print(f"Quintiles en datos: {quintiles_en_datos}")
print(f"Quintiles en paleta: {quintiles_en_paleta}")
if not quintiles_en_datos.issubset(quintiles_en_paleta):
    print(f"Quintiles faltantes en paleta: {quintiles_en_datos - quintiles_en_paleta}")
print()

# Mostrar estadísticas descriptivas
print("Estadísticas del coeficiente de variación:")
print(f"CV promedio: {resumen['cv'].mean():.2f}")
print(f"CV mediano: {resumen['cv'].median():.2f}")
print(f"CV mínimo: {resumen['cv'].min():.2f}")
print(f"CV máximo: {resumen['cv'].max():.2f}")
print("\nInterpretación:")
print("CV < 0.2: Poca variabilidad")
print("CV 0.2-0.5: Variabilidad moderada") 
print("CV > 0.5: Alta variabilidad")

# Graficar scatterplot
plt.figure(figsize=(12, 7))
sns.scatterplot(
    data=resumen,
    x='mean',
    y='std',
    size='count',
    hue='ivsmedia',  # Colorear por quintil
    sizes=(10, 200),  # Tamaño mínimo y máximo de burbujas
    alpha=0.7,
    edgecolor='black',
    palette=colores_quintiles  # Usar colores específicos para cada quintil
)

plt.title("Variabilidad de uso de estudiantes por grupo-centro", fontsize=14)
plt.xlabel("Promedio de días de conexión (estudiantes del grupo-centro)")
plt.ylabel("Desviación estándar (varianza entre estudiantes)")
plt.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()