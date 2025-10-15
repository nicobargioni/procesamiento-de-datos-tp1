"""
Funciones de transformación temporal del dataset de desastres naturales
"""

import pandas as pd
import numpy as np


def crear_columna_fecha(df, columna_año='Start Year', columna_mes='Start Month', columna_dia='Start Day'):
    """
    Crea una columna de fecha unificada a partir de año, mes y día

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame con los datos
    columna_año : str
        Nombre de la columna con el año
    columna_mes : str
        Nombre de la columna con el mes
    columna_dia : str
        Nombre de la columna con el día

    Retorna:
    --------
    pd.DataFrame
        DataFrame con la nueva columna 'fecha'
    """
    df_copy = df.copy()

    # Rellenar valores faltantes
    df_copy[columna_año] = df_copy[columna_año].fillna(df_copy['Year'])
    df_copy[columna_mes] = df_copy[columna_mes].fillna(1)  # Si no hay mes, usar enero
    df_copy[columna_dia] = df_copy[columna_dia].fillna(1)  # Si no hay día, usar día 1

    # Convertir a enteros para evitar problemas con decimales
    df_copy[columna_año] = df_copy[columna_año].astype(int)
    df_copy[columna_mes] = df_copy[columna_mes].astype(int)
    df_copy[columna_dia] = df_copy[columna_dia].astype(int)

    # Crear la columna fecha
    try:
        df_copy['fecha'] = pd.to_datetime(
            df_copy[[columna_año, columna_mes, columna_dia]].rename(
                columns={columna_año: 'year', columna_mes: 'month', columna_dia: 'day'}
            ),
            errors='coerce'
        )
    except Exception as e:
        print(f"Error al crear columna fecha: {e}")
        # Fallback: crear fecha solo con año y mes
        df_copy['fecha'] = pd.to_datetime(
            df_copy[columna_año].astype(str) + '-' + df_copy[columna_mes].astype(str),
            format='%Y-%m',
            errors='coerce'
        )

    print(f"✓ Columna 'fecha' creada. Valores válidos: {df_copy['fecha'].notna().sum()}/{len(df_copy)}")
    return df_copy


def filtrar_ultimas_decadas(df, columna_fecha='fecha', n_años=20):
    """
    Filtra el dataset para obtener solo las últimas n décadas

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame con los datos
    columna_fecha : str
        Nombre de la columna con la fecha
    n_años : int
        Número de años a considerar desde el año más reciente

    Retorna:
    --------
    pd.DataFrame
        DataFrame filtrado con las últimas décadas
    """
    df_copy = df.copy()

    # Obtener el año más reciente
    año_max = df_copy[columna_fecha].dt.year.max()
    año_inicio = año_max - n_años

    df_filtrado = df_copy[df_copy[columna_fecha].dt.year >= año_inicio]

    print(f"✓ Dataset filtrado: {len(df_filtrado)} registros desde {año_inicio} hasta {año_max}")
    return df_filtrado


def analizar_patrones_estacionales(df, columna_fecha='fecha'):
    """
    Analiza patrones estacionales en la ocurrencia de desastres

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame con los datos
    columna_fecha : str
        Nombre de la columna con la fecha

    Retorna:
    --------
    dict
        Diccionario con análisis estacionales
    """
    df_copy = df.copy()

    # Extraer componentes temporales
    df_copy['año'] = df_copy[columna_fecha].dt.year
    df_copy['mes'] = df_copy[columna_fecha].dt.month
    df_copy['mes_nombre'] = df_copy[columna_fecha].dt.month_name()
    df_copy['trimestre'] = df_copy[columna_fecha].dt.quarter
    df_copy['estacion'] = df_copy['mes'].apply(_asignar_estacion)

    # Análisis por mes
    por_mes = df_copy.groupby('mes').size().reset_index(name='cantidad')
    por_mes['mes_nombre'] = por_mes['mes'].apply(lambda x: pd.Timestamp(2000, x, 1).strftime('%B'))

    # Análisis por estación
    por_estacion = df_copy.groupby('estacion').size().reset_index(name='cantidad')

    # Análisis por trimestre
    por_trimestre = df_copy.groupby('trimestre').size().reset_index(name='cantidad')

    # Análisis por tipo de desastre y estación
    tipo_estacion = df_copy.groupby(['Disaster Type', 'estacion']).size().reset_index(name='cantidad')

    resultado = {
        'por_mes': por_mes,
        'por_estacion': por_estacion,
        'por_trimestre': por_trimestre,
        'tipo_estacion': tipo_estacion,
        'mes_mas_frecuente': por_mes.loc[por_mes['cantidad'].idxmax(), 'mes_nombre'],
        'estacion_mas_frecuente': por_estacion.loc[por_estacion['cantidad'].idxmax(), 'estacion']
    }

    print(f"\n=== ANÁLISIS DE PATRONES ESTACIONALES ===")
    print(f"Mes con más desastres: {resultado['mes_mas_frecuente']}")
    print(f"Estación con más desastres: {resultado['estacion_mas_frecuente']}")

    return resultado


def analizar_tendencias_temporales(df, columna_fecha='fecha', columna_tipo='Disaster Type'):
    """
    Analiza tendencias temporales en la ocurrencia de desastres

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame con los datos
    columna_fecha : str
        Nombre de la columna con la fecha
    columna_tipo : str
        Nombre de la columna con el tipo de desastre

    Retorna:
    --------
    dict
        Diccionario con análisis de tendencias
    """
    df_copy = df.copy()
    df_copy['año'] = df_copy[columna_fecha].dt.year

    # Tendencia anual general
    por_año = df_copy.groupby('año').size().reset_index(name='cantidad')

    # Tendencia por tipo de desastre
    tipo_año = df_copy.groupby(['año', columna_tipo]).size().reset_index(name='cantidad')

    # Calcular cambio porcentual año a año
    por_año['cambio_pct'] = por_año['cantidad'].pct_change() * 100

    # Top 5 tipos de desastres más frecuentes
    top_tipos = df_copy[columna_tipo].value_counts().head(5)

    resultado = {
        'por_año': por_año,
        'tipo_año': tipo_año,
        'top_tipos': top_tipos,
        'tendencia_promedio': por_año['cambio_pct'].mean(),
        'año_mayor_incidencia': por_año.loc[por_año['cantidad'].idxmax(), 'año']
    }

    print(f"\n=== ANÁLISIS DE TENDENCIAS TEMPORALES ===")
    print(f"Año con mayor incidencia: {resultado['año_mayor_incidencia']}")
    print(f"Tendencia promedio anual: {resultado['tendencia_promedio']:.2f}%")
    print(f"\nTop 5 tipos de desastres:")
    for tipo, cantidad in top_tipos.items():
        print(f"  - {tipo}: {cantidad} eventos")

    return resultado


def _asignar_estacion(mes):
    """
    Asigna una estación del año según el mes (Hemisferio Sur)

    Parámetros:
    -----------
    mes : int
        Número del mes (1-12)

    Retorna:
    --------
    str
        Nombre de la estación
    """
    if mes in [12, 1, 2]:
        return 'Verano'
    elif mes in [3, 4, 5]:
        return 'Otoño'
    elif mes in [6, 7, 8]:
        return 'Invierno'
    else:
        return 'Primavera'
