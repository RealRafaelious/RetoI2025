#################################################################################
# 3. ¿Los estudiantes que comparten docente muestran patrones de uso similares? #
#################################################################################

import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway, kruskal # Para comparar grupos (ANOVA o Kruskal-Wallis)

docentes_estudiantes = pd.reed_excel("/TablasActuales/UNION.xlsxs", sheet_name="DocentesEstudiantes")


