import pandas as pd

# ruta
excel_estudiantes = "TablasActuales/Tabla_estudiantes_7moa9no.xlsx"

# cargar
df_estudiantes = pd.read_excel(excel_estudiantes)

# noromalizar nombres de columnas  
df_estudiantes.columns = [col.strip().lower().replace(" ", "_") for col in df_estudiantes.columns]  

###############################################################################################
# 1. ¿Varía el uso de la plataforma CREA según el grado educativo? ¿Hay diferencias por sexo? #
###############################################################################################


#Detalles de estándares:
   # Grado educativo: 7mo, 8vo, 9no
   # Sexo: Masculino, Femenino
   # Se tomaron en cuenta dentro de la muestra aquellas personas que se hayan conectado 30 o más veces.
   
   
df_estudiantes.groupby('grado')['cr_total_dias_ingreso'].mean()

df_estudiantes.groupby('sexo')['cr_total_dias_ingreso'].mean()
 
df_estudiantes.groupby(['grado', 'sexo'])['cr_total_dias_ingreso'].mean()



