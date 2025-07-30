import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

###########################################################################################
# 2. ¿Hay diferencia entre el uso de CREA y la conexión por dispositivo? ¿Correlacionan?  #
###########################################################################################


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


# Contar casos
print("\n--- Resumen de Conexión Inicial ---")
print((df["dias_diferencia_crea_disp"] > 0).sum(), "estudiantes se conectaron primero al DISPOSITIVO")
print((df["dias_diferencia_crea_disp"] < 0).sum(), "estudiantes se conectaron primero a CREA")
print((df["dias_diferencia_crea_disp"] == 0).sum(), "estudiantes se conectaron el mismo día")

# Visualización 2: Dispersión entre días conectados y total días de ingreso con línea de tendencia
plt.figure(figsize=(8,6))
sns.regplot(y=col_total_dias, x=col_dias_disp, data=df, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
plt.title("Días de conexión vs Total días de ingreso con Línea de Tendencia")
plt.ylabel("Total días ingreso")
plt.xlabel("Días conexión dispositivo")
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
