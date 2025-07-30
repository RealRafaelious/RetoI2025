import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Cargar archivo combinado
df = pd.read_excel("TablasActuales/UNION.xlsx")

# Mostrar columnas (para verificar)
print("Columnas disponibles:", df.columns)

# Filtrar columnas directamente con los nombres reales
df_filtrado = df[["id_centro_docente", "grado_docente", "cr_total_dias_ingreso"]].dropna()

<<<<<<< HEAD

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
=======
# Crear columna combinada centro + grado
df_filtrado["centro_grado"] = df_filtrado["id_centro_docente"].astype(str) + " - " + df_filtrado["grado_docente"].astype(str)

# Agrupar por esa combinación
resumen = df_filtrado.groupby("centro_grado")["cr_total_dias_ingreso"].agg(["count", "mean", "std"])
resumen = resumen.sort_values("mean", ascending=False)

# Filtrar grupos con al menos 10 estudiantes
resumen_filtrado = resumen[resumen["count"] >= 10].head(20).reset_index()

# --- Gráfico de barras con barra de error ---
plt.figure(figsize=(16, 6))
x = np.arange(len(resumen_filtrado))
y = resumen_filtrado["mean"]
error = resumen_filtrado["std"]
labels = resumen_filtrado["centro_grado"]

plt.bar(x, y, yerr=error, capsize=5, color='lightblue', edgecolor='black')
plt.xticks(x, labels, rotation=90)
plt.title("Promedio de días de conexión a CREA por grupo y centro (con desviación estándar)")
plt.xlabel("Centro - Grado del docente")
plt.ylabel("Días de conexión a CREA")
plt.grid(axis='y', linestyle='--', alpha=0.6)
>>>>>>> 8ed6438903c7dba7b6b30506a822b4d8f22bb1cf
plt.tight_layout()
plt.show()

# --- Gráfico de boxplot por grupo-centro ---
df_top = df_filtrado[df_filtrado["centro_grado"].isin(resumen_filtrado["centro_grado"])]

plt.figure(figsize=(16, 6))
sns.boxplot(data=df_top, x="centro_grado", y="cr_total_dias_ingreso", color="lightgray")
plt.xticks(rotation=90)
plt.title("Distribución de días de conexión a CREA por grupo y centro")
plt.xlabel("Centro - Grado del docente")
plt.ylabel("Días de conexión a CREA")
plt.tight_layout()
plt.show()
