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
K = 4  # Podés cambiarlo según el gráfico del codo
modelo_final = KMeans(n_clusters=K, random_state=0)
df["cluster"] = modelo_final.fit_predict(X_scaled)
print("✅ Clustering aplicado correctamente")

# === 7. GUARDAR RESULTADO EN MISMA CARPETA QUE ESTE .PY ===
base_dir = os.path.dirname(os.path.abspath(__file__))
ruta_salida = os.path.join(base_dir, "UNION_clusters_usoCREA.xlsx")

try:
    df.to_excel(ruta_salida, index=False)
    print(f"✅ Archivo guardado en: {ruta_salida}")
except Exception as e:
    print(f"❌ Error al guardar el archivo: {e}")