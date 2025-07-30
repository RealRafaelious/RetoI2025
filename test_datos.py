import pandas as pd

try:
    # Cargar los datos
    print("Cargando datos...")
    df = pd.read_excel("TablasActuales/UNION.xlsx")
    print(f"Datos cargados: {len(df)} filas")
    
    # Mostrar las columnas disponibles
    print("\nPrimeras columnas disponibles:")
    print(df.columns.tolist()[:10])  # Solo las primeras 10
    
    # Verificar las columnas que necesitamos
    columnas_necesarias = ['grado_estudiante', 'grupo_estudiante', 'id_centro_docente']
    for col in columnas_necesarias:
        if col in df.columns:
            print(f"✓ {col} está disponible")
        else:
            print(f"✗ {col} NO está disponible")
    
    # Si tenemos las columnas, hacer el análisis
    if all(col in df.columns for col in columnas_necesarias):
        print("\n=== ANÁLISIS DE GRUPOS POR GRADO ===")
        
        # 1. Cuántos grupos hay de cada grado EN TOTAL
        grupos_por_grado = df.groupby('grado_estudiante')['grupo_estudiante'].nunique().sort_index()
        print("📊 GRUPOS POR GRADO (en todos los centros):")
        for grado, num_grupos in grupos_por_grado.items():
            print(f"   Grado {grado}: {num_grupos} grupos")
        
        print(f"\n🔢 TOTAL de grupos únicos: {df['grupo_estudiante'].nunique()}")
        
        # 2. Cuántos ESTUDIANTES hay por grado
        print("\n=== ANÁLISIS DE ESTUDIANTES POR GRADO ===")
        estudiantes_por_grado = df.groupby('grado_estudiante')['id_unico_estudiante'].nunique().sort_index()
        print("👥 ESTUDIANTES POR GRADO:")
        for grado, num_estudiantes in estudiantes_por_grado.items():
            print(f"   Grado {grado}: {num_estudiantes:,} estudiantes")
        
        print(f"\n🔢 TOTAL de estudiantes únicos: {df['id_unico_estudiante'].nunique():,}")
        
        # 3. Comparaciones directas
        print("\n=== COMPARACIONES ===")
        grado_7 = estudiantes_por_grado.get(7, 0)
        grado_8 = estudiantes_por_grado.get(8, 0)
        grado_9 = estudiantes_por_grado.get(9, 0)
        
        print("🔍 COMPARACIONES DE ESTUDIANTES:")
        if grado_9 > grado_7:
            diferencia = grado_9 - grado_7
            print(f"   ✓ SÍ, hay MÁS estudiantes en 9no ({grado_9:,}) que en 7mo ({grado_7:,})")
            print(f"     Diferencia: {diferencia:,} estudiantes más en 9no")
        else:
            diferencia = grado_7 - grado_9
            print(f"   ✗ NO, hay MÁS estudiantes en 7mo ({grado_7:,}) que en 9no ({grado_9:,})")
            print(f"     Diferencia: {diferencia:,} estudiantes más en 7mo")
        
        # 4. Promedio de estudiantes por grupo
        print("\n=== PROMEDIO DE ESTUDIANTES POR GRUPO ===")
        for grado in sorted(estudiantes_por_grado.index):
            num_estudiantes = estudiantes_por_grado[grado]
            num_grupos = grupos_por_grado[grado]
            promedio = num_estudiantes / num_grupos
            print(f"   Grado {grado}: {promedio:.1f} estudiantes por grupo promedio")
        
        # 5. Distribución por centro
        print("\n=== DISTRIBUCIÓN POR CENTRO ===")
        tabla_cruzada = pd.crosstab(df['id_centro_docente'], df['grado_estudiante'], 
                                   values=df['grupo_estudiante'], aggfunc='nunique', fill_value=0)
        print("📋 Grupos por grado en cada centro (Top 10 centros):")
        
        # Mostrar solo los 10 centros con más grupos totales
        centros_top = tabla_cruzada.sum(axis=1).sort_values(ascending=False).head(10)
        for centro in centros_top.index:
            fila = tabla_cruzada.loc[centro]
            print(f"   Centro {centro}: G7={fila.get(7,0)} | G8={fila.get(8,0)} | G9={fila.get(9,0)} grupos")
    else:
        # Mostrar todas las columnas para ayudar a identificar la correcta
        print("\nTodas las columnas disponibles:")
        for i, col in enumerate(df.columns):
            print(f"{i+1:2d}. {col}")
    
except Exception as e:
    print(f"Error: {e}")
