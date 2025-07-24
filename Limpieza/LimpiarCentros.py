import pandas as pd
import os

def limpiar_centros():
    # Leer archivo
    ruta_entrada = "TablasIniciales/Tabla_centros_7moa9no.xlsx"
    df = pd.read_excel(ruta_entrada)

    # Estandarizar nombres de columnas
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # ----------------------------
    # LIMPIEZA ROBUSTA
    # ----------------------------

    # 1. Reemplazar NaN reales por "sin identificar"
    df["ivsmedia"] = df["ivsmedia"].fillna("sin identificar")

    # 2. Convertir a string, quitar espacios y reemplazar vacíos por "sin identificar"
    df["ivsmedia"] = df["ivsmedia"].astype(str).str.strip()
    df.loc[df["ivsmedia"] == "", "ivsmedia"] = "sin identificar"

    # ----------------------------
    # VERIFICACIÓN
    # ----------------------------
    print("\nValores únicos después de limpiar:")
    print(df["ivsmedia"].unique())

    print(f'\nCantidad de "sin identificar": {(df["ivsmedia"] == "sin identificar").sum()}')
    print(f"Total de filas: {len(df)}")

     # Definir ruta de salida en carpeta TablasActuales
    carpeta_salida = "TablasActuales"
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)  # crear carpeta si no existe

    ruta_salida = os.path.abspath(os.path.join(carpeta_salida, "Tabla_centros_7moa9no_limpia.xlsx"))
    print(f"\nGuardando en: {ruta_salida}")

    try:
        df.to_excel(ruta_salida, index=False)
        print("\nArchivo guardado correctamente.")
    except PermissionError:
        print("\nNo se pudo guardar el archivo. Cerralo si lo tenés abierto en Excel.")

limpiar_centros()
