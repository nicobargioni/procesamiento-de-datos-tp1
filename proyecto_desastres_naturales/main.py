"""
Script Principal - Proceso ETL de Desastres Naturales
Ejecuta el pipeline completo de Extract, Transform, Load

Uso:
    python main.py
"""

import sys
import os
from pathlib import Path

# Asegurar que los módulos puedan ser importados
sys.path.append(str(Path(__file__).parent))

from extract.extract_data import cargar_dataset, validar_estructura, explorar_dataset
from transform.temporal_transform import (
    crear_columna_fecha,
    filtrar_ultimas_decadas,
    analizar_patrones_estacionales,
    analizar_tendencias_temporales
)
from transform.data_curation import (
    limpiar_tipo_desastre,
    limpiar_pais_region,
    crear_variables_derivadas
)
from load.visualizaciones import (
    crear_serie_temporal,
    crear_heatmap_estacional,
    crear_grafico_barras_tipo,
    crear_visualizacion_cruces,
    guardar_reporte
)

import matplotlib.pyplot as plt


def ejecutar_etl(ruta_dataset, generar_reporte_pdf=False):
    """
    Ejecuta el proceso ETL completo

    Parámetros:
    -----------
    ruta_dataset : str
        Ruta al archivo CSV del dataset
    generar_reporte_pdf : bool
        Si es True, genera un reporte PDF con todas las visualizaciones
    """
    print("=" * 70)
    print("PROCESO ETL - ANÁLISIS DE DESASTRES NATURALES (1970-2021)")
    print("=" * 70)

    # ====================
    # FASE 1: EXTRACCIÓN
    # ====================
    print("\n[1/3] FASE DE EXTRACCIÓN")
    print("-" * 70)

    # Cargar dataset
    df = cargar_dataset(ruta_dataset)

    # Validar estructura
    validacion = validar_estructura(df)
    if not validacion['valido']:
        print("✗ Error: El dataset no tiene la estructura requerida")
        return None

    # Explorar dataset
    exploracion = explorar_dataset(df)

    # ====================
    # FASE 2: TRANSFORMACIÓN
    # ====================
    print("\n[2/3] FASE DE TRANSFORMACIÓN")
    print("-" * 70)

    # Crear columna fecha
    print("\n→ Creando columna fecha unificada...")
    df = crear_columna_fecha(df)

    # Limpiar tipo de desastre
    print("\n→ Limpiando tipo de desastre...")
    df = limpiar_tipo_desastre(df)

    # Limpiar país y región
    print("\n→ Limpiando variables geográficas...")
    df = limpiar_pais_region(df)

    # Crear variables derivadas
    print("\n→ Creando variables derivadas...")
    df = crear_variables_derivadas(df)

    # Filtrar últimas dos décadas
    print("\n→ Filtrando últimas dos décadas (2001-2021)...")
    df_reciente = filtrar_ultimas_decadas(df, n_años=20)

    # Análisis temporal
    print("\n→ Analizando patrones estacionales...")
    analisis_estacional = analizar_patrones_estacionales(df_reciente)

    print("\n→ Analizando tendencias temporales...")
    tendencias = analizar_tendencias_temporales(df_reciente)

    # ====================
    # FASE 3: CARGA (VISUALIZACIÓN)
    # ====================
    print("\n[3/3] FASE DE CARGA Y VISUALIZACIÓN")
    print("-" * 70)

    figuras = []

    # Serie temporal
    print("\n→ Generando serie temporal...")
    fig1 = crear_serie_temporal(df_reciente)
    figuras.append(fig1)

    # Heatmap estacional
    print("→ Generando heatmap estacional...")
    fig2 = crear_heatmap_estacional(df_reciente)
    figuras.append(fig2)

    # Gráficos de barras
    print("→ Generando gráficos de distribución...")
    fig3 = crear_grafico_barras_tipo(df_reciente)
    figuras.append(fig3)

    # Cruces de variables
    print("\n→ Generando análisis de cruces de variables...")
    print("  1. Distribución geográfica de terremotos")
    fig4 = crear_visualizacion_cruces(df, 'terremotos_geo')
    figuras.append(fig4)

    print("  2. Regiones con mayor incidencia de inundaciones")
    fig5 = crear_visualizacion_cruces(df, 'inundaciones_region')
    figuras.append(fig5)

    print("  3. Patrones regionales de sequías")
    fig6 = crear_visualizacion_cruces(df, 'sequias_region')
    figuras.append(fig6)

    print("  4. Frecuencia de tormentas por continente")
    fig7 = crear_visualizacion_cruces(df, 'tormentas_continente')
    figuras.append(fig7)

    print("  5. Tendencia histórica de incendios forestales")
    fig8 = crear_visualizacion_cruces(df, 'incendios_tendencia')
    figuras.append(fig8)

    # Guardar reporte PDF si se solicita
    if generar_reporte_pdf:
        print("\n→ Guardando reporte PDF...")
        guardar_reporte(figuras, 'reporte_desastres_naturales.pdf')
    else:
        # Mostrar gráficos interactivamente
        print("\n→ Mostrando visualizaciones...")
        plt.show()

    # ====================
    # RESUMEN FINAL
    # ====================
    print("\n" + "=" * 70)
    print("RESUMEN DEL ANÁLISIS")
    print("=" * 70)

    print(f"\nDATOS PROCESADOS:")
    print(f"  • Total de eventos (1970-2021): {len(df):,}")
    print(f"  • Eventos en últimas dos décadas: {len(df_reciente):,}")
    print(f"  • Países afectados: {df['Country'].nunique()}")
    print(f"  • Regiones analizadas: {df['Region'].nunique()}")
    print(f"  • Tipos de desastres: {df['Disaster Type'].nunique()}")

    print(f"\nPATRONES IDENTIFICADOS:")
    print(f"  • Mes con más desastres: {analisis_estacional['mes_mas_frecuente']}")
    print(f"  • Estación con más desastres: {analisis_estacional['estacion_mas_frecuente']}")
    print(f"  • Año con mayor incidencia: {tendencias['año_mayor_incidencia']}")

    print(f"\nTOP 3 TIPOS DE DESASTRES:")
    top_tipos = df_reciente['Disaster Type'].value_counts().head(3)
    for i, (tipo, cantidad) in enumerate(top_tipos.items(), 1):
        pct = cantidad / len(df_reciente) * 100
        print(f"  {i}. {tipo}: {cantidad} ({pct:.1f}%)")

    print("\n" + "=" * 70)
    print("✓ PROCESO ETL COMPLETADO EXITOSAMENTE")
    print("=" * 70)

    return df, df_reciente, analisis_estacional, tendencias


def main():
    """
    Función principal
    """
    # Ruta al dataset (ajustar según ubicación)
    ruta_dataset = '../1970-2021_DISASTERS.xlsx - emdat data.csv'

    # Verificar que el archivo existe
    if not os.path.exists(ruta_dataset):
        print(f"✗ Error: No se encontró el archivo {ruta_dataset}")
        print(f"  Por favor, ajustar la ruta en el script main.py")
        return

    # Ejecutar ETL
    try:
        resultado = ejecutar_etl(
            ruta_dataset=ruta_dataset,
            generar_reporte_pdf=False  # Cambiar a True para generar PDF
        )

        if resultado:
            print("\n💡 Sugerencia: Abre el notebook 'analisis_desastres_naturales.ipynb'")
            print("   para ver el análisis completo con interpretaciones detalladas.")

    except Exception as e:
        print(f"\n✗ Error durante la ejecución: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
