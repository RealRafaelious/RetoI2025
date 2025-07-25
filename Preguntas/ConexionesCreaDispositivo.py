import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

# Ruta del archivo
archivo = r"..\TablasActuales\Tabla_estudiantes_7moa9no_limpia.xlsx"

# Cargar datos
df = pd.read_excel(archivo)

col_uso_crea = "primera_conexion_crea"
col_conexion_disp = "primera_conexion_dispositivo"
col_total_dias = "cr_total_dias_ingreso"
col_dias_conexion_disp = "dias_de_conexion_dispositivo"


# Estadísticas descriptivas básicas
print(df[[col_uso_crea, col_conexion_disp, col_total_dias, col_dias_conexion_disp]].describe())

# Visualización distribuciones de las conexiones
plt.figure(figsize=(12,6))
plt.subplot(1,2,1)
sns.histplot(df[col_uso_crea].dropna(), kde=True)
plt.title("Distribución Primera conexión CREA")

plt.subplot(1,2,2)
sns.histplot(df[col_conexion_disp].dropna(), kde=True)
plt.title("Distribución Primera conexión Dispositivo")

plt.tight_layout()
plt.show()

# Scatterplot de dias de conexion dispositivo vs total dias ingreso (ejemplo de relación)
plt.figure(figsize=(6,6))
sns.scatterplot(data=df, x=col_total_dias, y=col_dias_conexion_disp)
plt.title("Días de conexión dispositivo vs Total días de ingreso")
plt.show()

# Correlación entre primera conexión CREA y primera conexión dispositivo


# Convertir fechas si son fechas
if pd.api.types.is_datetime64_any_dtype(df[col_uso_crea]):
    df[col_uso_crea] = df[col_uso_crea].map(lambda x: x.toordinal() if pd.notnull(x) else None)
if pd.api.types.is_datetime64_any_dtype(df[col_conexion_disp]):
    df[col_conexion_disp] = df[col_conexion_disp].map(lambda x: x.toordinal() if pd.notnull(x) else None)

# Drop NaNs para correlación
df_corr = df[[col_uso_crea, col_conexion_disp]].dropna()

corr, p_value = pearsonr(df_corr[col_uso_crea], df_corr[col_conexion_disp])
print(f"Correlación Pearson entre primera conexión CREA y primera conexión dispositivo: {corr:.3f}")
print(f"P-valor: {p_value:.3e}")
if p_value < 0.05:
    print("Correlación estadísticamente significativa.")
else:
    print("No hay evidencia estadística suficiente para afirmar correlación.")

# Promedios ejemplo
print(f"Promedio días ingreso (total): {df[col_total_dias].mean():.2f}")
print(f"Promedio días de conexión dispositivo: {df[col_dias_conexion_disp].mean():.2f}")