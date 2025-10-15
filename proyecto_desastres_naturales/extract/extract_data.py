"""
Funciones de extracción de datos del dataset de desastres naturales
"""

import pandas as pd
import os


def cargar_dataset(ruta_archivo):
    """
    Carga el dataset de desastres naturales desde un archivo CSV

    Parámetros:
    -----------
    ruta_archivo : str
        Ruta al archivo CSV con los datos de desastres

    Retorna:
    --------
    pd.DataFrame
        DataFrame con los datos cargados

    Raises:
    -------
    FileNotFoundError
        Si el archivo no existe en la ruta especificada
    ValueError
        Si el archivo está vacío o no se puede leer correctamente
    """
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo {ruta_archivo} no existe")

    try:
        df = pd.read_csv(ruta_archivo, encoding='utf-8')
    except UnicodeDecodeError:
        # Intentar con otra codificación si UTF-8 falla
        df = pd.read_csv(ruta_archivo, encoding='latin-1')

    if df.empty:
        raise ValueError("El dataset está vacío")

    print(f"Dataset cargado exitosamente: {df.shape[0]} filas y {df.shape[1]} columnas")
    return df


def validar_estructura(df):
    """
    Valida que el dataset contenga las columnas esenciales para el análisis

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame a validar

    Retorna:
    --------
    dict
        Diccionario con información sobre la validación
    """
    columnas_requeridas = [
        'Year', 'Start Month', 'Disaster Type', 'Country', 'Region', 'Continent'
    ]

    columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]

    resultado = {
        'valido': len(columnas_faltantes) == 0,
        'columnas_faltantes': columnas_faltantes,
        'total_columnas': len(df.columns),
        'columnas_presentes': list(df.columns)
    }

    if resultado['valido']:
        print("✓ Todas las columnas requeridas están presentes")
    else:
        print(f"✗ Faltan columnas requeridas: {columnas_faltantes}")

    return resultado


def explorar_dataset(df):
    """
    Realiza una exploración inicial del dataset

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame a explorar

    Retorna:
    --------
    dict
        Diccionario con estadísticas descriptivas del dataset
    """
    exploracion = {
        'forma': df.shape,
        'columnas': list(df.columns),
        'tipos_datos': df.dtypes.to_dict(),
        'valores_nulos': df.isnull().sum().to_dict(),
        'porcentaje_nulos': (df.isnull().sum() / len(df) * 100).to_dict(),
        'primeras_filas': df.head(),
        'rango_temporal': {
            'año_min': df['Year'].min() if 'Year' in df.columns else None,
            'año_max': df['Year'].max() if 'Year' in df.columns else None
        }
    }

    print("\n=== EXPLORACIÓN INICIAL DEL DATASET ===")
    print(f"Dimensiones: {exploracion['forma'][0]} filas × {exploracion['forma'][1]} columnas")
    print(f"\nRango temporal: {exploracion['rango_temporal']['año_min']} - {exploracion['rango_temporal']['año_max']}")
    print(f"\nColumnas con más valores nulos:")

    # Mostrar top 10 columnas con más valores nulos
    nulos_ordenados = sorted(exploracion['porcentaje_nulos'].items(),
                            key=lambda x: x[1], reverse=True)[:10]
    for col, pct in nulos_ordenados:
        if pct > 0:
            print(f"  - {col}: {pct:.2f}%")

    return exploracion
