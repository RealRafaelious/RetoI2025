import pandas as pd

# ver excel
df = pd.read_excel(r'C:\Users\Estudiante UCU\Repositorios\RetoI2025\Tabla_centros_7moa9no.xlsx')

# contar celdas con valor "desconocido"
cantidad = (df['IvsMedia'].isna()).sum()

print(f'Cantidad de celdas con valor nulo: {cantidad}')

# cantidad total de datos
cantidad = len(df)
print(f'Cantidad total de datos: {cantidad}')