import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os

# === 1. LEER EL EXCEL ===
df = pd.read_excel("TablasActuales/UNION.xlsx")

# === 1.1 EXTRAER QUINTIL DESDE 'ivsmedia' ===
df["quintil"] = df["ivsmedia"].astype(str).str.extract(r"(\d)").astype(float)

# === 2. SELECCIONAR VARIABLES DE USO DE CREA ===
columnas_crea = ["cr_total_dias_ingreso", "dias_de_conexion_dispositivo", "grado_estudiante", "quintil"]
X = df[columnas_crea].dropna()
print("\n📄 Primeras 5 filas del DataFrame original seleccionado:")
print(X.head())

# === 3. SINCRONIZAR df CON X ===
df = df.loc[X.index].copy()

# === 4. ESCALAR LOS DATOS ===
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("\n🔍 Primeras 5 filas escaladas:")
print(X_scaled[:5])

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
K = 4  # Cambiar según el gráfico del codo
modelo_final = KMeans(n_clusters=K, random_state=0)
df["cluster"] = modelo_final.fit_predict(X_scaled)
print("✅ Clustering aplicado correctamente")

# === 6.1 CALCULAR MEDIA DE CADA CLUSTER ===
medias_cluster = df.groupby("cluster")[columnas_crea].mean().round(2)
print("\n📊 Media de cada variable por cluster:")
print(medias_cluster)


# === 7. GUARDAR RESULTADO DEL CLUSTERING EN EXCEL ===
base_dir = os.path.dirname(os.path.abspath(__file__))
ruta_salida = os.path.join(base_dir, "UNION_clusters_usoCREA.xlsx")

try:
    df.to_excel(ruta_salida, index=False)
    print(f"✅ Archivo guardado en: {ruta_salida}")
except Exception as e:
    print(f"❌ Error al guardar el archivo: {e}")

# === 8. GUARDAR RESUMEN DE MEDIAS EN EXCEL ===
ruta_medias = os.path.join(base_dir, "Resumen_medias_clusters.xlsx")

try:
    medias_cluster.to_excel(ruta_medias)
    print(f"✅ Archivo de resumen guardado en: {ruta_medias}")
except Exception as e:
    print(f"❌ Error al guardar el archivo de medias: {e}")