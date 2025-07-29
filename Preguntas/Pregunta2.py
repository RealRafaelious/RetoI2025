import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

# Cargar datos
archivo = "./TablasActuales/Tabla_estudiantes_7moa9no_limpia.xlsx"
df = pd.read_excel(archivo)

# Nombres de columnas
col_crea_fecha = "primera_conexion_crea"
col_disp_fecha = "primera_conexion_dispositivo"
col_total_dias = "cr_total_dias_ingreso"
col_dias_disp = "dias_de_conexion_dispositivo"

# Convertir fechas
df[col_crea_fecha] = pd.to_datetime(df[col_crea_fecha], errors="coerce")
df[col_disp_fecha] = pd.to_datetime(df[col_disp_fecha], errors="coerce")

# Crear columna de diferencia de días
df["dias_diferencia_crea_disp"] = (df[col_crea_fecha] - df[col_disp_fecha]).dt.days

# Visualización 1: Histograma de diferencias de fechas
plt.figure(figsize=(10,5))
sns.histplot(df["dias_diferencia_crea_disp"].dropna(), bins=50, kde=True)
plt.axvline(0, color='red', linestyle='--')
plt.title("Diferencia en días entre primera conexión CREA y Dispositivo")
plt.xlabel("Días (positivos: CREA después, negativos: CREA antes)")
plt.tight_layout()
plt.show()

# Contar casos
print("\n--- Resumen de Conexión Inicial ---")
print((df["dias_diferencia_crea_disp"] > 0).sum(), "estudiantes se conectaron primero al DISPOSITIVO")
print((df["dias_diferencia_crea_disp"] < 0).sum(), "estudiantes se conectaron primero a CREA")
print((df["dias_diferencia_crea_disp"] == 0).sum(), "estudiantes se conectaron el mismo día")

# Visualización 2: Dispersión entre días conectados y total días de ingreso
plt.figure(figsize=(8,6))
sns.scatterplot(x=col_total_dias, y=col_dias_disp, data=df, alpha=0.5)
plt.title("Días de conexión vs Total días de ingreso")
plt.xlabel("Total días ingreso")
plt.ylabel("Días conexión dispositivo")
plt.tight_layout()
plt.show()

# Visualización 3: Relación CREA vs dispositivo en términos de días
plt.figure(figsize=(8,6))
sns.scatterplot(x=col_dias_disp, y=col_total_dias, data=df, alpha=0.5)
plt.title("Días conexión dispositivo vs Total días ingreso")
plt.xlabel("Días conexión dispositivo")
plt.ylabel("Total días ingreso")
plt.tight_layout()
plt.show()

# Correlación entre fechas de conexión
df_corr = df[[col_crea_fecha, col_disp_fecha]].dropna()
if not df_corr.empty:
    crea_ordinal = df_corr[col_crea_fecha].map(lambda x: x.toordinal())
    disp_ordinal = df_corr[col_disp_fecha].map(lambda x: x.toordinal())
    corr, p = pearsonr(crea_ordinal, disp_ordinal)

    print(f"\nCorrelación entre fechas de primera conexión CREA y Dispositivo: r = {corr:.3f}")
    print(f"P-valor: {p:.2e}")
    if p < 0.05:
        print("✅ Correlación significativa.")
    else:
        print("❌ No hay correlación significativa.")
else:
    print("No hay suficientes datos para correlación de fechas.")

# Promedios
print(f"\nPromedio días ingreso: {df[col_total_dias].mean():.2f}")
print(f"Promedio días conexión dispositivo: {df[col_dias_disp].mean():.2f}")
