# Hackathon-
Repositorio para alojar el programa

## integrantes 
Silvia Juliana Mancilla Padilla
Jossue Alejandro Eugenio Triana
Miguel Ángel Esparza Bernal

## Fuente de Datos

Los datos utilizados en este proyecto provienen del catálogo oficial de sismicidad histórica y en tiempo real del **Servicio Geológico Colombiano (SGC)**:

* **Sitio Web Oficial:** [Servicio Geológico Colombiano - Consulta de Sismos](https://www.sgc.gov.co/sismos)
* **Cobertura Espacial:** Departamento de Santander y zonas aledañas (Colombia).
* **Periodo de Registro:** Sismos registrados entre los años 1993 y 2026.
* **Volumen:** $214.833$ registros sísmicos procesados y depurados.

# Flujo de Procesamiento Paso a Paso

###  Justificación de Variables

Las variables seleccionadas del catálogo oficial del **Servicio Geológico Colombiano (SGC)** responden a criterios geofísicos y de calidad de medición:

1. **Variables Físicas Principales:** `magnitude`, `depth`, `latitude`, `longitude` — Definen la posición espacial (hipocentro) y la energía liberada, factores determinantes en el cálculo del impacto superficial.
2. **Métricas de Calidad Sísmica:** `rms`, `gap`, `nst` — Miden el error de tiempo de onda, la cobertura angular de los sensores y la cantidad de estaciones, garantizando la precisión de la triangulación.
3. **Métricas de Incertidumbre:** `magnitude_error`, `depth_error`, `latitude_error`, `longitude_error` — Determinan el margen de error instrumental para la robustez del modelo.
4. **Temporal y Target:** `local_time` (monitoreo temporal) y `nivel_riesgo` (clasificación basada en norma técnica NSR-10).

1. **Carga y Limpieza de Datos:**
   * Carga el dataset procesado (`sismos_santander_procesado.csv`).
   * Valida la integridad del dataset asegurando la presencia de las variables físicas fundamentales (`magnitude`, `depth`, `latitude`, `longitude`).

2. **Categorización de Riesgo Objetivo (Regla Técnica):**
   * Evalúa la relación entre magnitud y profundidad epicentral mediante la función `assign_risk`:
     * **Alto:** Magnitud e 4.0, o magnitud  3.0 con profundidad superficial (< 30t{km}).
     * **Medio:** Magnitud entre 2.5 y $3.9
     * **Bajo:** Magnitudes < 2.5

3. **Imputación y Preparación de Variables Predictoras:**
   * Selecciona 11 variables técnicas y de calidad sísmica (`magnitude`, `depth`, `latitude`, `longitude`, `rms`, `gap`, `nst` y errores de medición).
   * Rrellena valores faltantes en las métricas con la **mediana** (`.fillna(df.median())`), garantizando la robustez del modelo.

4. **Entrenamiento del Modelo (Random Forest Classifier):**
   * Divide los datos en un **80% para entrenamiento** y un **20% para prueba**, utilizando **muestreo estratificado** (`stratify=y`) para mantener la proporción de clases.
   * Entrena un ensamble de bosques aleatorios (`n_estimators=50`, `max_depth=10`) para clasificar de manera precisa los eventos sísmicos.

5. **Módulo de Recomendaciones de Ingeniería (NSR-10):**
   * Asigna automáticamente recomendaciones técnicas a cada registro según la predicción del modelo:
     *  **Alto:** *"Atención: Es indispensable aplicar un diseño estructural estricto bajo la norma NSR-10. Se requiere estudio geotécnico de detalle para mitigar efectos de amplificación."*
     *  **Medio:** *"Precaución: Se aconseja supervisión rigurosa en los cálculos de ingeniería y verificación de la capacidad portante del suelo."*
     *  **Bajo:** *"Zona Favorable: El terreno presenta condiciones estables; mantener los parámetros estándar de construcción sismorresistente."*

6. **Métricas y Exportación a Power BI:**
   * Imprime en consola el reporte de clasificación completo y la precisión global del modelo (*Accuracy*).
   * Genera la tabla final `df_clean` y el resumen `df_metricas` para su integración e higienización directa en tableros de **Power BI**.
  
   * https://drive.google.com/drive/folders/1WJm08VodhfUN3MRG-BJfKTYM-9ok6LkB?usp=sharing
