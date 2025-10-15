"""
Funciones de curación y limpieza de datos del dataset de desastres naturales
"""

import pandas as pd
import numpy as np


def limpiar_tipo_desastre(df, columna='Disaster Type'):
    """
    Limpia y estandariza la columna de tipo de desastre

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame con los datos
    columna : str
        Nombre de la columna a limpiar

    Retorna:
    --------
    pd.DataFrame
        DataFrame con la columna limpia
    """
    df_copy = df.copy()

    if columna not in df_copy.columns:
        print(f"✗ La columna '{columna}' no existe en el dataset")
        return df_copy

    # Eliminar espacios en blanco
    df_copy[columna] = df_copy[columna].str.strip()

    # Contar valores nulos antes de la limpieza
    nulos_antes = df_copy[columna].isnull().sum()

    # Imputar valores faltantes con la moda
    if nulos_antes > 0:
        moda = df_copy[columna].mode()[0]
        df_copy[columna] = df_copy[columna].fillna(moda)
        print(f"✓ {nulos_antes} valores nulos imputados con '{moda}'")

    # Estandarizar nombres (capitalizar primera letra)
    df_copy[columna] = df_copy[columna].str.title()

    # Mostrar distribución
    print(f"\nDistribución de tipos de desastre:")
    distribucion = df_copy[columna].value_counts()
    for tipo, cantidad in distribucion.head(10).items():
        print(f"  - {tipo}: {cantidad} ({cantidad/len(df_copy)*100:.2f}%)")

    return df_copy


def limpiar_pais_region(df, columna_pais='Country', columna_region='Region'):
    """
    Limpia y estandariza las columnas de país y región

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame con los datos
    columna_pais : str
        Nombre de la columna de país
    columna_region : str
        Nombre de la columna de región

    Retorna:
    --------
    pd.DataFrame
        DataFrame con las columnas limpias
    """
    df_copy = df.copy()

    # Limpiar columna de país
    if columna_pais in df_copy.columns:
        df_copy[columna_pais] = df_copy[columna_pais].str.strip()
        nulos_pais = df_copy[columna_pais].isnull().sum()

        if nulos_pais > 0:
            print(f"⚠ Hay {nulos_pais} valores nulos en '{columna_pais}' ({nulos_pais/len(df_copy)*100:.2f}%)")
            # No imputar países, mantener como desconocido
            df_copy[columna_pais] = df_copy[columna_pais].fillna('Unknown')

    # Limpiar columna de región
    if columna_region in df_copy.columns:
        df_copy[columna_region] = df_copy[columna_region].str.strip()
        nulos_region = df_copy[columna_region].isnull().sum()

        if nulos_region > 0:
            print(f"⚠ Hay {nulos_region} valores nulos en '{columna_region}' ({nulos_region/len(df_copy)*100:.2f}%)")
            df_copy[columna_region] = df_copy[columna_region].fillna('Unknown')

    print(f"\n✓ Columnas geográficas limpiadas")
    print(f"Total de países: {df_copy[columna_pais].nunique()}")
    print(f"Total de regiones: {df_copy[columna_region].nunique()}")

    return df_copy


def normalizar_columnas(df, columnas_numericas=None):
    """
    Normaliza columnas numéricas del dataset

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame con los datos
    columnas_numericas : list
        Lista de columnas numéricas a normalizar

    Retorna:
    --------
    pd.DataFrame
        DataFrame con columnas normalizadas
    """
    df_copy = df.copy()

    if columnas_numericas is None:
        # Columnas numéricas comunes en el dataset
        columnas_numericas = [
            'Total Deaths', 'No Injured', 'No Affected',
            'No Homeless', 'Total Affected', 'Total Damages (\'000 US$)'
        ]

    for columna in columnas_numericas:
        if columna in df_copy.columns:
            # Convertir a numérico (por si hay valores no numéricos)
            df_copy[columna] = pd.to_numeric(df_copy[columna], errors='coerce')

            # Crear columna normalizada
            columna_norm = f'{columna}_norm'
            valores = df_copy[columna].dropna()

            if len(valores) > 0:
                min_val = valores.min()
                max_val = valores.max()

                if max_val > min_val:
                    df_copy[columna_norm] = (df_copy[columna] - min_val) / (max_val - min_val)
                else:
                    df_copy[columna_norm] = 0

                print(f"✓ Columna '{columna}' normalizada")

    return df_copy


def imputar_valores_faltantes(df, estrategia='media', columnas=None):
    """
    Imputa valores faltantes en columnas numéricas

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame con los datos
    estrategia : str
        Estrategia de imputación: 'media', 'mediana', 'moda', 'cero'
    columnas : list
        Lista de columnas a imputar. Si es None, se imputan todas las numéricas

    Retorna:
    --------
    pd.DataFrame
        DataFrame con valores imputados
    """
    df_copy = df.copy()

    if columnas is None:
        # Seleccionar solo columnas numéricas
        columnas = df_copy.select_dtypes(include=[np.number]).columns.tolist()

    print(f"\n=== IMPUTACIÓN DE VALORES FALTANTES ===")
    print(f"Estrategia: {estrategia}")

    for columna in columnas:
        if columna in df_copy.columns:
            nulos = df_copy[columna].isnull().sum()

            if nulos > 0:
                if estrategia == 'media':
                    valor_imputacion = df_copy[columna].mean()
                elif estrategia == 'mediana':
                    valor_imputacion = df_copy[columna].median()
                elif estrategia == 'moda':
                    valor_imputacion = df_copy[columna].mode()[0]
                elif estrategia == 'cero':
                    valor_imputacion = 0
                else:
                    print(f"⚠ Estrategia '{estrategia}' no reconocida. Usando 'media'")
                    valor_imputacion = df_copy[columna].mean()

                df_copy[columna] = df_copy[columna].fillna(valor_imputacion)
                print(f"  - {columna}: {nulos} valores imputados ({nulos/len(df_copy)*100:.2f}%)")

    return df_copy


def crear_variables_derivadas(df):
    """
    Crea variables derivadas útiles para el análisis

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame con los datos

    Retorna:
    --------
    pd.DataFrame
        DataFrame con nuevas variables
    """
    df_copy = df.copy()

    # Severidad del desastre (basada en muertes y afectados)
    if 'Total Deaths' in df_copy.columns and 'Total Affected' in df_copy.columns:
        df_copy['severidad'] = pd.cut(
            df_copy['Total Deaths'].fillna(0) + df_copy['Total Affected'].fillna(0) * 0.01,
            bins=[-np.inf, 100, 1000, 10000, np.inf],
            labels=['Baja', 'Media', 'Alta', 'Extrema']
        )

    # Década
    if 'Year' in df_copy.columns:
        df_copy['decada'] = (df_copy['Year'] // 10) * 10

    print(f"✓ Variables derivadas creadas")

    return df_copy
