import pandas as pd

# Cargar el archivo Excel (reemplaza 'archivo.xlsx' por el nombre de tu archivo)
df = pd.read_excel('archivo.xlsx')

# Supongamos que la columna que quieres revisar se llama 'grupo'
# Contar cuántas celdas tienen el valor "desconocido"
cantidad = (df['grupo'] == 'desconocido').sum()

print(f'Cantidad de celdas con valor "desconocido": {cantidad}')
