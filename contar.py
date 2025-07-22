import pandas as pd

# Cargar el archivo Excel (reemplaza 'archivo.xlsx' por el nombre de tu archivo)
df = pd.read_excel(r'C:\Users\Estudiante UCU\Repositorios\RetoI2025\Tabla_estudiantes_7moa9no_limpia.xlsx')

# Supongamos que la columna que quieres revisar se llama 'grupo'
# Contar cuántas celdas tienen el valor "desconocido"
cantidad = (df['grupo'] == 'desconocido').sum()

print(f'Cantidad de celdas con valor "desconocido": {cantidad}')
