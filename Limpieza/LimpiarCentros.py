import pandas as pd

def limpiar_centros():  
    # ruta
    centrosxlsx = "TablasIniciales/Tabla_centros_7moa9no.xlsx"
    df = pd.read_excel(centrosxlsx)
    #estandarización de datos
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Filtrar filas donde ivsmedia no sea NaN ni cadena vacía
    df_limpio = df[df["ivsmedia"].notna() & (df["ivsmedia"].astype(str).str.strip() != "")]

    print(f"Filas eliminadas por ivsmedia vacía o NaN: {len(df) - len(df_limpio)}")

    # Guardar archivo limpio
    try:
        df_limpio.to_excel(
            r"../Tabla_centros_7moa9no_limpia.xlsx",
            index=False
        )
    except PermissionError:
        print("No se pudo guardar el archivo. Cerralo si lo tenés abierto en Excel.")


    print("Limpieza completada.")
    print(f"Centros con quintil guardados: {df_limpio.shape[0]}")
    print(f'Cantidad de celdas con valor nulo en ivsmedia original: {df["ivsmedia"].isna().sum()}')
