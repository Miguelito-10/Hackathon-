import pandas as pd

# 1. Cargar el dataset original
df = pd.read_csv('C:/Users/Lenovo/Documents/jossue/competencia/sismos.csv')
print(f"Registros totales iniciales: {len(df)}")

# 2. Filtrar solo registros manuales (mayor confiabilidad técnica)
df_clean = df[df['status'] == 'manual'].copy()

# 3. Seleccionar las variables clave justificadas
selected_cols = [
    'magnitude', 'depth', 'latitude', 'longitude', 
    'rms', 'gap', 'nst', 'magnitude_error', 
    'depth_error', 'latitude_error', 'longitude_error', 'local_time'
]
df_clean = df_clean[selected_cols]

# 4. Limpieza de valores nulos en variables físicas críticas
df_clean = df_clean.dropna(subset=['magnitude', 'depth', 'latitude', 'longitude'])

# 5. Crear la variable dependiente (Target): 'nivel_riesgo'
# Criterio técnico basado en magnitud y profundidad (sismos superficiales y de mayor energía = mayor riesgo)
def assign_risk(row):
    mag = row['magnitude']
    dep = row['depth']
    if mag >= 4.0 or (mag >= 3.0 and dep < 30):
        return 'Alto'
    elif mag >= 2.5:
        return 'Medio'
    else:
        return 'Bajo'

df_clean['nivel_riesgo'] = df_clean.apply(assign_risk, axis=1)

# 6. Mostrar resumen del resultado
print("\nDistribución de las clases de riesgo creadas:")
print(df_clean['nivel_riesgo'].value_counts(normalize=True) * 100)

# 7. Guardar el dataset listo para el modelado
df_clean.to_csv('sismos_santander_procesado.csv', index=False)
print("\n¡Dataset procesado guardado exitosamente como 'sismos_santander_procesado.csv'!")