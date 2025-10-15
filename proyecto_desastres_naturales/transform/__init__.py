"""
Módulo de Transformación de Datos
Contiene funciones para transformar, limpiar y curar el dataset de desastres naturales
"""

from .temporal_transform import (
    crear_columna_fecha,
    filtrar_ultimas_decadas,
    analizar_patrones_estacionales,
    analizar_tendencias_temporales
)

from .data_curation import (
    limpiar_tipo_desastre,
    limpiar_pais_region,
    normalizar_columnas,
    imputar_valores_faltantes
)

__all__ = [
    'crear_columna_fecha',
    'filtrar_ultimas_decadas',
    'analizar_patrones_estacionales',
    'analizar_tendencias_temporales',
    'limpiar_tipo_desastre',
    'limpiar_pais_region',
    'normalizar_columnas',
    'imputar_valores_faltantes'
]
