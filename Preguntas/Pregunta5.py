# 5. ¿El sexo del docente influye en el nivel de conexión de sus estudiantes? #
#################################################################################
import pandas as pd
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar archivo unido
df = pd.read_excel("TablasActuales/UNION.xlsx")

# Filtrar columnas necesarias y eliminar nulos
df_filtrado = df[["sexo_docente", "dias_de_conexion_dispositivo"]].dropna()

# Separar grupos
mujeres = df_filtrado[df_filtrado["sexo_docente"] == "F"]["dias_de_conexion_dispositivo"]
varones = df_filtrado[df_filtrado["sexo_docente"] == "M"]["dias_de_conexion_dispositivo"]

# Calcular medias
prom_mujeres = mujeres.mean()
prom_varones = varones.mean()

# Prueba estadística
t_stat, p_value = ttest_ind(mujeres, varones)

# Mostrar resultados
print("Promedio conexión (docente mujer):", round(prom_mujeres, 2))
print("Promedio conexión (docente varón):", round(prom_varones, 2))
print("p-valor:", round(p_value, 5))

if p_value < 0.05:
    print("El sexo del docente influye en la conexión (diferencia significativa).")
else:
    print("No hay evidencia significativa de que influya el sexo del docente.")

# ---------------------------------
# Gráfico: distribución de conexión por sexo docente
# ---------------------------------
plt.figure(figsize=(8, 6))
sns.boxplot(data=df_filtrado, x="sexo_docente", y="dias_de_conexion_dispositivo", palette="pastel")
plt.title("Días de conexión del estudiante según sexo del docente")
plt.xlabel("Sexo del docente")
plt.ylabel("Días de conexión del estudiante")
plt.xticks(ticks=[0, 1], labels=["Mujer", "Varón"])
plt.grid(True)
plt.tight_layout()

# Mostrar la gráfica
plt.show() 
