import pandas as pd
import os

# ruta del directorio
directorio = "C:/Users/Estudiante UCU/Repositorios/RetoI2025/"

# obtener todos los archivos excel csv menos los limpios
archivos = [f for f in os.listdir(directorio) if f.endswith(('.xlsx', '.csv')) and 'limpia' not in f.lower()]

for archivo in archivos:
    ruta_completa = os.path.join(directorio, archivo)
    print(f"limpiando: {archivo}")

    try:

        # detectar tipo de archivo
        if archivo.endswith('.csv'):
            df = pd.read_csv(ruta_completa, encoding='utf-8', sep=None, engine='python')
        elif archivo.endswith('.xlsx'):
            df = pd.read_excel(ruta_completa)

        # eliminar fila con todos los valores vacios
        df = df.dropna(how='all')

        # sacar espacios
        for col in df.select_dtypes(include='object'):
             df[col] = df[col].str.strip()

        # nomralizar nomnres
        df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]


        # guardar archivo
        nombre_limpio = archivo.replace('.xlsx', '_limpia.xlsx')
        ruta_salida = ruta_completa
        
        if archivo.endswith('.csv'):
            df.to_csv(ruta_salida, index=False, encoding='utf-8')
        else:
            df.to_excel(ruta_salida, index=False)

        print(f"guardado como: {nombre_limpio}")

    except Exception as e:
        print(f"error procesando {archivo}: {e}")

print("OK")










 

