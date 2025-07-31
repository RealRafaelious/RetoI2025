import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import os

# === 1. LEER EL EXCEL ===
df = pd.read_excel("Preguntas/UNION_clusters_usoCREA.xlsx")

# Agrupar por cluster y contar quintiles
medias_cluster = df.groupby('cluster')['ivsmedia'].value_counts().unstack(fill_value=0).reset_index()

# Transformar a formato largo para graficar
quintil_por_cluster = medias_cluster.melt(
    id_vars='cluster',
    var_name='ivsmedia',
    value_name='Count'
)

# Mostrar tabla
print(quintil_por_cluster)

# Crear gráfico con Clúster en el eje X y Quintil como hue
plt.figure(figsize=(10, 6))
sns.barplot(
    data=quintil_por_cluster,
    x='cluster',
    y='Count',
    hue='ivsmedia'  # ahora el color indica el quintil
)
plt.title('Distribución de Clusters por Quintil')
plt.xlabel('Cluster')
plt.ylabel('Cantidad')
plt.legend(title='Quintil')
plt.tight_layout()
plt.show()