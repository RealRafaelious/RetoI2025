import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os

# === 1. LEER EL EXCEL ===
df = pd.read_excel("TablasActuales/UNION.xlsx")

# === 2. SELECCIONAR VARIABLES DE USO DE CREA ===
columnas_crea = ["cr_total_dias_ingreso", "dias_de_conexion_dispositivo", "edad_estudiante"]
X = df[columnas_crea].dropna()

# === 3. SINCRONIZAR df CON X ===
df = df.loc[X.index].copy()

# === 4. ESCALAR LOS DATOS ===
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# === 5. MÉTODO DEL CODO PARA DEFINIR K ===
inercia = []
for k in range(1, 10):
    modelo = KMeans(n_clusters=k, random_state=0)
    modelo.fit(X_scaled)
    inercia.append(modelo.inertia_)

plt.plot(range(1, 10), inercia, marker='o')
plt.title("Método del Codo")
plt.xlabel("Número de clusters")
plt.ylabel("Inercia")
plt.grid(True)
plt.show()

# === 6. ENTRENAR KMEANS CON K ELEGIDO ===
K = 4  # Cambiá este valor si querés
modelo_final = KMeans(n_clusters=K, random_state=0)
df["cluster"] = modelo_final.fit_predict(X_scaled)
print("✅ Clustering aplicado correctamente")

# === 7. OBTENER CENTROIDES ===

# A. En escala estandarizada (no muy útil para interpretar)
print("\n📍 Centroides (escalados):")
print(modelo_final.cluster_centers_)

# B. En valores originales (interpretables)
centroides_originales = scaler.inverse_transform(modelo_final.cluster_centers_)
centroides_df = pd.DataFrame(centroides_originales, columns=columnas_crea)

print("\n📌 Centroides (valores reales/desescalados):")
print(centroides_df.round(2))

# === 8. GUARDAR RESULTADO DEL CLUSTERING ===
base_dir = os.path.dirname(os.path.abspath(__file__))
ruta_salida_clusters = os.path.join(base_dir, "UNION_clusters_usoCREA2.xlsx")
ruta_salida_centroides = os.path.join(base_dir, "UNION_centroides.xlsx")

try:
    df.to_excel(ruta_salida_clusters, index=False)
    centroides_df.to_excel(ruta_salida_centroides, index=False)
    print(f"\n✅ Archivos guardados:")
    print(f"   - Resultados con clusters → {ruta_salida_clusters}")
    print(f"   - Centroides por cluster  → {ruta_salida_centroides}")
except Exception as e:
    print(f"❌ Error al guardar los archivos: {e}")