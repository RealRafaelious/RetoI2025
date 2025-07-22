import pandas as pd
import os

# ruta del directorio
directorio = "C:/Users/Estudiante UCU/Repositorios/RetoI2025/"

# obtener todos los archivos excel menos los limpios
archivos = [f for f in os.listdir(directorio) if f.endswith('.xlsx') and 'limpia' not in f.lower()]

for archivo in archivos:
    ruta_completa = os.path.join(directorio, archivo)
    print(f"limpiando: {archivo}")

    try:
        df = pd.read_excel(ruta_completa)

        # eliminar fila con todos los valores vacios
        df = df.dropna(how='all')

        # cambiar nulo por texto sin datos
        df = df.fillna("Sin datos")

        # sacar espacios
        for col in df.select_dtypes(include='object'):
             df[col] = df[col].str.strip() 

        # guardar archivo
        nombre_limpio = archivo.replace('.xlsx', '_limpia.xlsx')
        ruta_limpia = os.path.join(directorio, nombre_limpio)
        df.to_excel(ruta_limpia, index=False)

        print(f"guardado como: {nombre_limpio}")

    except Exception as e:
        print(f"error procesando {archivo}: {e}")

print("OK")










 

