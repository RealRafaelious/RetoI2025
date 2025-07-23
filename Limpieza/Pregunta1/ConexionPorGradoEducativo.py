import pandas as pd

# ruta
archivo = "TablasActuales/Tabla_estudiantes_7moa9no.xlsx"

# cargar
df = pd.read_excel(archivo)

# noromalizar nombres de columnas
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

###############################################################################################
# 1. ¿Varía el uso de la plataforma CREA según el grado educativo? ¿Hay diferencias por sexo? #
###############################################################################################


#Detalles de estándares:
   # Grado educativo: 7mo, 8vo, 9no
   # Sexo: Masculino, Femenino
   # Se tomaron en cuenta dentro de la muestra aquellas personas que se hayan conectado 30 o más veces.
   
 