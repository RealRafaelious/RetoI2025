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

# Normalizar nombres de columnas
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Nombres de columnas
col_crea_fecha = "primera_conexion_crea"
col_disp_fecha = "primera_conexion_dispositivo"
col_total_dias = "cr_total_dias_ingreso" # Asumo que esta es la columna de "Total días ingreso a CREA"
col_dias_disp = "dias_de_conexion_dispositivo" # Asumo que esta es la columna de "Días conexión dispositivo"
col_grado = "grado" # Columna para separar por grados

# Convertir fechas (si es necesario y no se hizo en un script anterior)
df[col_crea_fecha] = pd.to_datetime(df[col_crea_fecha], errors="coerce")
df[col_disp_fecha] = pd.to_datetime(df[col_disp_fecha], errors="coerce")

# Crear columna de diferencia de días
df["dias_diferencia_crea_disp"] = (df[col_crea_fecha] - df[col_disp_fecha]).dt.days

# Asegurarse de que la columna 'grado' sea string y minúscula para consistencia
df[col_grado] = df[col_grado].astype(str).str.strip().str.lower()

# Filtrar para grados 7, 8, 9 y establecer orden (esto ya se hacía)
orden_grados = ['7', '8', '9']
df = df[df[col_grado].isin(orden_grados)].copy()
df[col_grado] = pd.Categorical(df[col_grado], categories=orden_grados, ordered=True)


# Contar casos
print("\n--- Resumen de Conexión Inicial ---")
print((df["dias_diferencia_crea_disp"] > 0).sum(), "estudiantes se conectaron primero al DISPOSITIVO")
print((df["dias_diferencia_crea_disp"] < 0).sum(), "estudiantes se conectaron primero a CREA")
print((df["dias_diferencia_crea_disp"] == 0).sum(), "estudiantes se conectaron el mismo día")

# Promedios (repetidos aquí para mayor claridad en la salida)
print(f"\nPromedio días ingreso: {df[col_total_dias].mean():.2f}")
print(f"Promedio días conexión dispositivo: {df[col_dias_disp].mean():.2f}")


# --- Gráfica Original: Todos los grados juntos ---
plt.figure(figsize=(10, 7))
sns.regplot(y=col_total_dias, x=col_dias_disp, data=df, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
plt.title("Días de conexión vs Total días de ingreso con Línea de Tendencia (Todos los Grados)")
plt.ylabel("Total días ingreso a CREA")
plt.xlabel("Días conexión dispositivo")
plt.ylim(bottom=0) # Asegura que el eje Y empiece en 0
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()


# --- Nuevas Gráficas: Separadas por Grado ---

print("\n--- Visualización: Días de conexión vs Total días de ingreso (Separado por Grado) ---")

for grado_actual in orden_grados:
    df_grado = df[df[col_grado] == grado_actual].copy()

    if not df_grado.empty:
        plt.figure(figsize=(10, 7))
        sns.regplot(y=col_total_dias, x=col_dias_disp, data=df_grado, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
        plt.title(f"Días de conexión vs Total días de ingreso (Grado {grado_actual})")
        plt.ylabel("Total días ingreso a CREA")
        plt.xlabel("Días conexión dispositivo")
        plt.ylim(bottom=0) # Asegura que el eje Y empiece en 0
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()
    else:
        print(f"No hay datos para el Grado {grado_actual} después del filtrado.")


# --- Correlación entre fechas de conexión (se mantiene igual) ---
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