import pandas as pd

# cargar archivo

df = pd.read_excel("Tabla_estudiantes_7moa9no.xlsx")

# ver
print(df.head())
print(df.info())

