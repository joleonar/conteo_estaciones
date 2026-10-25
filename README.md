# Conteo de Fases P por Estación Sísmica

Herramienta en Python para el procesamiento, conteo mensual acumulativo y visualización (mapas de calor) de las detecciones de arribo de onda P por estación sismológica a partir de archivos de salida de SEISAN (`select.out`).

---

## 📌 Descripción

El flujo de trabajo automatiza la extracción de fases sísmicas P asociadas a cada estación y mantiene una base de datos histórica incremental en formato JSON (`historico_estaciones.json`). 

Esto elimina la necesidad de conservar o reprocesar los archivos `select_*.out` de meses pasados:
- Se procesa únicamente el archivo del mes actual.
- Se integra automáticamente al histórico existente (mediante `outer join`, asignando 0 a meses previos si aparece una nueva estación).
- Se genera una figura en alta resolución (`Estaciones2026.png`) mostrando el mapa de calor mensual acumulado.

---

## 🗂 Estructura del Proyecto

```text
├── cuenta_estaciones.py         # Módulo parser de fases P desde select.out
├── actualizar_y_graficar.py     # Script principal: actualiza JSON y crea el heatmap
├── historico_estaciones.json    # Base de datos acumulativa (estaciones vs meses)
├── Estaciones2026.png           # Imagen generada del mapa de calor
├── requirements.txt             # Dependencias del proyecto
└── README.md                    # Documentación