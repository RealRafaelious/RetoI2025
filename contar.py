import pandas as pd

# ver excel
df = pd.read_excel(r'C:\Users\Estudiante UCU\Repositorios\RetoI2025\Tabla_estudiantes_7moa9no_limpia.xlsx')

# contar celdas con valor "desconocido"
cantidad = (df['grupo'] == 'desconocido').sum()

print(f'Cantidad de celdas con valor "desconocido": {cantidad}')

# cantidad total de datos
cantidad = len(df)
print(f'Cantidad total de datos: {cantidad}')