#################################################################################
# 5. ¿El sexo del docente influye en el nivel de conexión de sus estudiantes? #
#################################################################################
import pandas as pd
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar archivo unido
df = pd.read_excel("TablasActuales/UNION.xlsx")

print("LIMITACIÓN METODOLÓGICA:")
print("Los 'dias_de_conexion_dispositivo' son globales por estudiante, no específicos por docente/materia.")
print("Por tanto, no podemos establecer relación causal directa entre sexo del docente y conexión.")
print("\nENFOQUE ALTERNATIVO: Análisis por grupos")
print("="*60)

# Crear identificador de grupo-centro
df['id_grupo'] = df['ciclo_docente'].astype(str) + '_' + df['id_centro_docente'].astype(str)

print("DEFINICIÓN DE GRUPO:")
print("Grupo = ciclo_docente + id_centro_docente")
print("Ejemplo: '7_15' = ciclo 7 en centro 15")
print("Asumimos que estudiantes del mismo ciclo en el mismo centro forman un 'grupo'")
print(f"Total de grupos únicos identificados: {df['id_grupo'].nunique()}")
print(f"Total de registros (estudiante-docente): {len(df)}")
print()

# Explorar la composición de sexo por grupo
print("ANÁLISIS DE COMPOSICIÓN DE GRUPOS:")
print("="*50)

# Verificar cuántos sexos diferentes hay por grupo
grupos_sexo = df.groupby('id_grupo')['sexo_docente'].nunique().reset_index()
grupos_sexo.columns = ['id_grupo', 'num_sexos_diferentes']

print("Distribución de grupos por número de sexos de docentes:")
print(grupos_sexo['num_sexos_diferentes'].value_counts().sort_index())

# Mostrar algunos ejemplos de grupos con múltiples sexos
grupos_mixtos = grupos_sexo[grupos_sexo['num_sexos_diferentes'] > 1]['id_grupo'].head(5)
if len(grupos_mixtos) > 0:
    print(f"\nEjemplos de grupos con docentes de ambos sexos:")
    for grupo in grupos_mixtos:
        sexos_en_grupo = df[df['id_grupo'] == grupo]['sexo_docente'].unique()
        print(f"Grupo {grupo}: {sexos_en_grupo}")

print("\nCRITERIO ACTUAL PROBLEMÁTICO:")
print("- Estamos tomando el sexo del docente de cualquier fila del grupo")
print("- Esto es arbitrario si hay docentes de ambos sexos en el grupo")
print("- No refleja verdadero 'liderazgo' del grupo")

# Mostrar criterios posibles
print("\nCRITERIOS ALTERNATIVOS POSIBLES:")
print("1. Tomar el sexo más frecuente en el grupo")
print("2. Excluir grupos mixtos del análisis")
print("3. Analizar solo grupos con un único sexo de docente")
print("4. Usar proporción de docentes por sexo como variable continua")

# Filtrar columnas necesarias y eliminar nulos
df_filtrado = df[["id_grupo", "sexo_docente", "dias_de_conexion_dispositivo"]].dropna()

# CRITERIO MEJORADO: Analizar composición de sexo por grupo
def obtener_sexo_predominante(serie):
    """Función segura para obtener el sexo predominante o único en un grupo"""
    serie_limpia = serie.dropna()
    if len(serie_limpia) == 0:
        return None
    moda = serie_limpia.mode()
    return moda.iloc[0] if len(moda) > 0 else None

grupos_composicion = df_filtrado.groupby('id_grupo')['sexo_docente'].agg([
    'nunique', 
    obtener_sexo_predominante
]).reset_index()
grupos_composicion.columns = ['id_grupo', 'num_sexos', 'sexo_predominante']

# Eliminar grupos sin información de sexo
grupos_composicion = grupos_composicion.dropna(subset=['sexo_predominante'])

# Calcular promedio de conexión por grupo
grupos_conexion = df_filtrado.groupby('id_grupo').agg(
    promedio_conexion=('dias_de_conexion_dispositivo', 'mean'),
    num_estudiantes=('dias_de_conexion_dispositivo', 'count')
).reset_index()

# Combinar información
grupos_resumen = grupos_conexion.merge(grupos_composicion, on='id_grupo')

print(f"\nTOTAL DE GRUPOS: {len(grupos_resumen)}")
print(f"Grupos con un solo sexo de docente: {len(grupos_resumen[grupos_resumen['num_sexos'] == 1])}")
print(f"Grupos con ambos sexos: {len(grupos_resumen[grupos_resumen['num_sexos'] > 1])}")

# OPCIÓN 1: Analizar solo grupos con un único sexo de docente
grupos_puros = grupos_resumen[grupos_resumen['num_sexos'] == 1].copy()
grupos_puros['sexo_docente'] = grupos_puros['sexo_predominante']

# Validar que tenemos grupos puros
if len(grupos_puros) == 0:
    print("\n❌ ERROR: No hay grupos con un único sexo de docente para analizar.")
    print("El análisis no puede proceder.")
    exit()

# Validar que tenemos ambos sexos representados
grupos_f = grupos_puros[grupos_puros['sexo_docente'] == 'F']
grupos_m = grupos_puros[grupos_puros['sexo_docente'] == 'M']

if len(grupos_f) == 0 or len(grupos_m) == 0:
    print(f"\n⚠️  ADVERTENCIA: Solo tenemos grupos de un sexo:")
    print(f"Grupos con docentes mujeres: {len(grupos_f)}")
    print(f"Grupos con docentes varones: {len(grupos_m)}")
    print("No es posible hacer comparación estadística.")

print(f"\nANÁLISIS CON GRUPOS 'PUROS' (un solo sexo):")
print(f"Grupos con solo docentes mujeres: {len(grupos_f)}")
print(f"Grupos con solo docentes varones: {len(grupos_m)}")

# Validar tamaño mínimo de grupos para análisis estadístico
if len(grupos_f) < 3 or len(grupos_m) < 3:
    print(f"\n⚠️  ADVERTENCIA: Grupos muy pequeños para análisis estadístico robusto")
    print(f"Se recomienda al menos 3 grupos por categoría para t-test confiable")

# Separar grupos por sexo del docente (solo grupos puros)
grupos_mujeres = grupos_puros[grupos_puros["sexo_docente"] == "F"]["promedio_conexion"]
grupos_varones = grupos_puros[grupos_puros["sexo_docente"] == "M"]["promedio_conexion"]

print(f"Número de grupos con docente mujer: {len(grupos_mujeres)}")
print(f"Número de grupos con docente varón: {len(grupos_varones)}")

# Calcular estadísticas descriptivas
if len(grupos_mujeres) > 0 and len(grupos_varones) > 0:
    prom_grupos_mujeres = grupos_mujeres.mean()
    prom_grupos_varones = grupos_varones.mean()
    
    print(f"\n📊 ESTADÍSTICAS DESCRIPTIVAS:")
    print(f"Grupos con docentes mujeres:")
    print(f"  - Promedio: {prom_grupos_mujeres:.2f} días")
    print(f"  - Desviación estándar: {grupos_mujeres.std():.2f}")
    print(f"  - Mediana: {grupos_mujeres.median():.2f}")
    
    print(f"Grupos con docentes varones:")
    print(f"  - Promedio: {prom_grupos_varones:.2f} días")
    print(f"  - Desviación estándar: {grupos_varones.std():.2f}")
    print(f"  - Mediana: {grupos_varones.median():.2f}")
    
    # Prueba estadística
    if len(grupos_mujeres) >= 3 and len(grupos_varones) >= 3:
        t_stat, p_value = ttest_ind(grupos_mujeres, grupos_varones)
        print(f"\n🧮 PRUEBA ESTADÍSTICA (t-test):")
        print(f"Estadístico t: {t_stat:.4f}")
        print(f"p-valor: {p_value:.5f}")
        
        if p_value < 0.05:
            print("✅ Hay diferencia estadísticamente significativa entre grupos según sexo del docente (α=0.05).")
        else:
            print("❌ No hay diferencia estadísticamente significativa entre grupos según sexo del docente (α=0.05).")
            
        # Calcular tamaño del efecto
        diferencia = abs(prom_grupos_mujeres - prom_grupos_varones)
        pooled_std = ((grupos_mujeres.std()**2 + grupos_varones.std()**2) / 2)**0.5
        cohens_d = diferencia / pooled_std if pooled_std > 0 else 0
        print(f"Tamaño del efecto (Cohen's d): {cohens_d:.3f}")
        
        if cohens_d < 0.2:
            print("  → Efecto pequeño/negligible")
        elif cohens_d < 0.5:
            print("  → Efecto pequeño")
        elif cohens_d < 0.8:
            print("  → Efecto mediano")
        else:
            print("  → Efecto grande")
    else:
        print(f"\n⚠️  Muestra insuficiente para t-test confiable.")
        print(f"Grupos con mujeres: {len(grupos_mujeres)}, con varones: {len(grupos_varones)}")
        
else:
    print("❌ No hay datos suficientes para realizar análisis estadístico.")

print("\nIMPORTANTE: Este análisis tiene limitaciones:")
print("- Los estudiantes pueden tener múltiples docentes")
print("- Los días de conexión son globales, no por materia específica")
print("- La relación podría estar confundida por otros factores")

# ---------------------------------
# Gráfico: promedio de conexión por grupo según sexo docente (solo grupos puros)
# ---------------------------------
plt.figure(figsize=(10, 6))
sns.boxplot(data=grupos_puros, x="sexo_docente", y="promedio_conexion", palette="pastel")
plt.title("Promedio de conexión por grupo según sexo del docente\n(Solo grupos con un único sexo de docente)")
plt.xlabel("Sexo del docente")
plt.ylabel("Promedio de días de conexión del grupo")
plt.xticks(ticks=[0, 1], labels=["Mujer", "Varón"])
plt.grid(True, alpha=0.3)

# Agregar información sobre el número de grupos
plt.text(0.02, 0.98, f'Grupos con solo docentes mujeres: {len(grupos_mujeres)}', 
         transform=plt.gca().transAxes, verticalalignment='top', fontsize=10)
plt.text(0.02, 0.92, f'Grupos con solo docentes varones: {len(grupos_varones)}', 
         transform=plt.gca().transAxes, verticalalignment='top', fontsize=10)
plt.text(0.02, 0.86, f'Grupos mixtos excluidos: {len(grupos_resumen) - len(grupos_puros)}', 
         transform=plt.gca().transAxes, verticalalignment='top', fontsize=10)

plt.tight_layout()
plt.show()

print("\nCONCLUSIÓN:")
print("Este análisis es exploratorio y tiene limitaciones importantes.")
print("Para una respuesta definitiva necesitaríamos:")
print("- Datos de conexión específicos por materia")
print("- Control por variables confusoras (nivel socioeconómico, centro, etc.)")
print("- Información sobre asignación de estudiantes a docentes") 
