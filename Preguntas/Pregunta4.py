#################################################################################
# 4. ¿Los estudiantes que comparten docente muestran patrones de uso similares? #
#################################################################################
import pandas as pd
from scipy.stats import f_oneway
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar archivo unido
df = pd.read_excel("TablasActuales/UNION.xlsx")

# Filtrar columnas necesarias y eliminar nulos
df_filtrado = df[["id_unico_docente", "dias_de_conexion_dispositivo"]].dropna()

# agrupar por docente 
agrupado = df_filtrado.groupby("id_unico_docente")["dias_de_conexion_dispositivo"]
resumen = agrupado.agg(["count", "mean", "std"]).sort_values("count", ascending=False)
print("\nResumen por docente:")
print(resumen.head())


# grafico de barras
plt.figure(figsize=(14, 6))
sns.barplot(data=resumen.reset_index(),
            x="id_unico_docente", 
            y="mean",
            palette="crest"
)
plt.xticks(rotation=90)
plt.title("Promedio de días de conexión por docente")
plt.xlabel("Docente")
plt.ylabel("Días de conexión promedio")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Visualizar con boxplot
plt.figure(figsize=(12, 6))
sns.boxplot(data=df_filtrado, x="id_unico_docente", y="dias_de_conexion_dispositivo")
plt.xticks(rotation=90)
plt.title("Distribución de conexión por docente")
plt.xlabel("Docente")
plt.ylabel("Días de conexión")
plt.tight_layout()
plt.show()

# varianza para ver diferecias significativas
# conexiones por docente

grupos = [grupo["dias_de_conexion_dispositivo"].values for _, grupo in df_filtrado.groupby("id_unico_docente") if len(grupo) > 1]

# al menos dos validos para varianza
if len(grupos) >= 2:
    f_stat, p_value = f_oneway(*grupos)
    print(f"\nANOVA F = {f_stat:.3f}, p = {p_value:.4f}")
    if p_value < 0.05:
        print("Hay diferencias significativas entre los grupos de docentes.")
    else:
        print("No hay diferencias significativas entre los grupos de docentes.")
else:
    print("No hay suficientes grupos para realizar ANOVA.")
