import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from cuenta_estaciones import cuenta_estaciones

# --- Configuración ---
DB_JSON = 'historico_estaciones.json'
ARCHIVO_NUEVO = 'select.out'   # El archivo del mes que deseas incorporar
MES_NUEVO = 'sep'              # Etiqueta de columna para este mes

# Estaciones que no deseas incluir en el reporte final
NO_INCLUIR = [
    'ACPR','ACTION','ARGC','ANWB','BAR2','BCIP','BBGH','BIM','CRJC','FLO2',
    'GCMP','GRGR','HEL','JTS','LCBC','MTDJ','NOR','OCA','OLDACT','ROSC',
    'RUS','SJC','TAM','TRN', 'URE','URI','ZAR'
]

# Orden cronológico de los meses para asegurar la secuencia en el gráfico
ORDEN_MESES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']

# 1. Cargar histórico si existe
if os.path.exists(DB_JSON):
    df_historico = pd.read_json(DB_JSON, orient='index')
else:
    df_historico = pd.DataFrame()

# 2. Procesar el mes nuevo
if os.path.exists(ARCHIVO_NUEVO):
    df_mes = cuenta_estaciones(ARCHIVO_NUEVO, nombre_columna=MES_NUEVO)
    
    if df_historico.empty:
        df_historico = df_mes
    else:
        # Si el mes ya estaba, lo reemplazamos con los datos nuevos
        if MES_NUEVO in df_historico.columns:
            df_historico = df_historico.drop(columns=[MES_NUEVO])
        
        # Merge outer preservando todas las estaciones
        df_historico = df_historico.merge(df_mes, left_index=True, right_index=True, how='outer')
    
    # Rellenar NaN con ceros y convertir a enteros
    df_historico = df_historico.fillna(0).astype(int)
    
    # Guardar estado actualizado en JSON
    df_historico.to_json(DB_JSON, orient='index', indent=4)
    print(f"-> Base de datos actualizada con el mes: {MES_NUEVO}")
else:
    print(f"Aviso: {ARCHIVO_NUEVO} no encontrado. Se graficará con los datos históricos existentes.")

# 3. Filtrar y ordenar para la gráfica
df_grafica = df_historico.copy()

# Eliminar estaciones descartadas que estén presentes en el índice
estaciones_a_borrar = [sta for sta in NO_INCLUIR if sta in df_grafica.index]
df_grafica = df_grafica.drop(index=estaciones_a_borrar)

# Ordenar las columnas cronológicamente según los meses disponibles
columnas_ordenadas = [m for m in ORDEN_MESES if m in df_grafica.columns]
df_grafica = df_grafica[columnas_ordenadas]

# 4. Generar Mapa de Calor
fig, ax = plt.subplots(figsize=(8, 11), dpi=300)
sns.heatmap(df_grafica, ax=ax, cmap='RdBu_r', annot=True, fmt='d', cbar_kws={'label': 'Nº de fases P'})

ax.set_title('Nº sismos detectados por estación en 2026', fontsize=14, pad=12)
ax.set_ylabel('')
ax.set_xlabel('')
plt.tight_layout()

salida_img = 'conteo_estaciones2026.png'
plt.savefig(salida_img, dpi=300)
print(f"-> Gráfico guardado en: {salida_img}")