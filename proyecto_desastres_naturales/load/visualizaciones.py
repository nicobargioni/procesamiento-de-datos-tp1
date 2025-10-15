"""
Funciones de visualización para el análisis de desastres naturales
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime


# Configuración de estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


def crear_serie_temporal(df, columna_fecha='fecha', columna_tipo='Disaster Type',
                         titulo='Serie Temporal de Desastres Naturales',
                         top_tipos=5):
    """
    Crea una serie temporal de la ocurrencia de desastres

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame con los datos
    columna_fecha : str
        Nombre de la columna con la fecha
    columna_tipo : str
        Nombre de la columna con el tipo de desastre
    titulo : str
        Título del gráfico
    top_tipos : int
        Número de tipos de desastres más frecuentes a mostrar

    Retorna:
    --------
    matplotlib.figure.Figure
        Figura con el gráfico
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

    # Serie temporal general
    df_temporal = df.set_index(columna_fecha).resample('Y').size()
    ax1.plot(df_temporal.index, df_temporal.values, linewidth=2, color='steelblue', marker='o')
    ax1.set_title(f'{titulo} - Tendencia Anual', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Año', fontsize=12)
    ax1.set_ylabel('Cantidad de Desastres', fontsize=12)
    ax1.grid(True, alpha=0.3)

    # Serie temporal por tipo de desastre (top N)
    tipos_frecuentes = df[columna_tipo].value_counts().head(top_tipos).index

    for tipo in tipos_frecuentes:
        df_tipo = df[df[columna_tipo] == tipo].set_index(columna_fecha).resample('Y').size()
        ax2.plot(df_tipo.index, df_tipo.values, linewidth=2, marker='o', label=tipo, alpha=0.8)

    ax2.set_title(f'Tendencia por Tipo de Desastre (Top {top_tipos})', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Año', fontsize=12)
    ax2.set_ylabel('Cantidad de Desastres', fontsize=12)
    ax2.legend(loc='best', fontsize=10)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def crear_heatmap_estacional(df, columna_fecha='fecha', columna_tipo='Disaster Type'):
    """
    Crea un heatmap de patrones estacionales

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
    matplotlib.figure.Figure
        Figura con el heatmap
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Heatmap mes vs año
    df_copy = df.copy()
    df_copy['año'] = df_copy[columna_fecha].dt.year
    df_copy['mes'] = df_copy[columna_fecha].dt.month

    pivot_mes_año = df_copy.groupby(['año', 'mes']).size().reset_index(name='cantidad')
    pivot_mes_año = pivot_mes_año.pivot(index='mes', columns='año', values='cantidad')

    sns.heatmap(pivot_mes_año, cmap='YlOrRd', cbar_kws={'label': 'Cantidad de Desastres'},
                ax=ax1, linewidths=0.5, fmt='g')
    ax1.set_title('Heatmap: Mes vs Año', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Año', fontsize=12)
    ax1.set_ylabel('Mes', fontsize=12)

    # Heatmap tipo de desastre vs mes
    tipos_principales = df[columna_tipo].value_counts().head(8).index
    df_tipos = df_copy[df_copy[columna_tipo].isin(tipos_principales)]

    pivot_tipo_mes = df_tipos.groupby([columna_tipo, 'mes']).size().reset_index(name='cantidad')
    pivot_tipo_mes = pivot_tipo_mes.pivot(index=columna_tipo, columns='mes', values='cantidad')

    sns.heatmap(pivot_tipo_mes, cmap='viridis', cbar_kws={'label': 'Cantidad'},
                ax=ax2, linewidths=0.5, fmt='g', annot=True)
    ax2.set_title('Heatmap: Tipo de Desastre vs Mes', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Mes', fontsize=12)
    ax2.set_ylabel('Tipo de Desastre', fontsize=12)

    plt.tight_layout()
    return fig


def crear_distribucion_geografica(df, columna_region='Region', columna_tipo='Disaster Type',
                                  filtro_tipo=None, top_n=15):
    """
    Crea visualización de distribución geográfica de desastres

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame con los datos
    columna_region : str
        Nombre de la columna con la región
    columna_tipo : str
        Nombre de la columna con el tipo de desastre
    filtro_tipo : str
        Tipo de desastre específico a analizar (opcional)
    top_n : int
        Número de regiones a mostrar

    Retorna:
    --------
    matplotlib.figure.Figure
        Figura con el gráfico
    """
    fig, ax = plt.subplots(figsize=(14, 8))

    if filtro_tipo:
        df_filtrado = df[df[columna_tipo] == filtro_tipo]
        titulo = f'Distribución Geográfica - {filtro_tipo}'
    else:
        df_filtrado = df
        titulo = 'Distribución Geográfica - Todos los Desastres'

    # Contar por región
    distribucion = df_filtrado[columna_region].value_counts().head(top_n)

    # Crear gráfico de barras horizontales
    colores = plt.cm.viridis(np.linspace(0, 1, len(distribucion)))
    distribucion.plot(kind='barh', ax=ax, color=colores)

    ax.set_title(titulo, fontsize=14, fontweight='bold')
    ax.set_xlabel('Cantidad de Desastres', fontsize=12)
    ax.set_ylabel('Región', fontsize=12)
    ax.invert_yaxis()

    # Añadir valores en las barras
    for i, v in enumerate(distribucion.values):
        ax.text(v + max(distribucion.values) * 0.01, i, f'{v}',
                va='center', fontsize=10, fontweight='bold')

    plt.tight_layout()
    return fig


def crear_grafico_barras_tipo(df, columna_tipo='Disaster Type', columna_agrupacion='Continent',
                              top_tipos=8, top_grupos=10):
    """
    Crea gráfico de barras agrupadas por tipo de desastre

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame con los datos
    columna_tipo : str
        Nombre de la columna con el tipo de desastre
    columna_agrupacion : str
        Columna por la cual agrupar (ej: 'Continent', 'Region')
    top_tipos : int
        Número de tipos de desastres a mostrar
    top_grupos : int
        Número de grupos a mostrar

    Retorna:
    --------
    matplotlib.figure.Figure
        Figura con el gráfico
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Gráfico 1: Distribución general de tipos
    tipos = df[columna_tipo].value_counts().head(top_tipos)
    colores = plt.cm.Set3(np.linspace(0, 1, len(tipos)))

    tipos.plot(kind='bar', ax=ax1, color=colores, edgecolor='black', linewidth=1.2)
    ax1.set_title(f'Top {top_tipos} Tipos de Desastres', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Tipo de Desastre', fontsize=12)
    ax1.set_ylabel('Cantidad', fontsize=12)
    ax1.tick_params(axis='x', rotation=45, labelsize=10)

    # Añadir valores encima de las barras
    for i, v in enumerate(tipos.values):
        ax1.text(i, v + max(tipos.values) * 0.01, f'{v}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Gráfico 2: Distribución por grupo
    grupos = df[columna_agrupacion].value_counts().head(top_grupos)
    colores2 = plt.cm.Paired(np.linspace(0, 1, len(grupos)))

    grupos.plot(kind='bar', ax=ax2, color=colores2, edgecolor='black', linewidth=1.2)
    ax2.set_title(f'Top {top_grupos} {columna_agrupacion}', fontsize=14, fontweight='bold')
    ax2.set_xlabel(columna_agrupacion, fontsize=12)
    ax2.set_ylabel('Cantidad de Desastres', fontsize=12)
    ax2.tick_params(axis='x', rotation=45, labelsize=10)

    for i, v in enumerate(grupos.values):
        ax2.text(i, v + max(grupos.values) * 0.01, f'{v}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.tight_layout()
    return fig


def crear_analisis_comparativo(df, tipo_desastre, columna_tipo='Disaster Type',
                               columnas_impacto=['Total Deaths', 'Total Affected']):
    """
    Crea análisis comparativo de impacto por tipo de desastre

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame con los datos
    tipo_desastre : str
        Tipo de desastre específico a analizar
    columna_tipo : str
        Nombre de la columna con el tipo de desastre
    columnas_impacto : list
        Columnas de impacto a visualizar

    Retorna:
    --------
    matplotlib.figure.Figure
        Figura con el análisis
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()

    df_filtrado = df[df[columna_tipo] == tipo_desastre].copy()

    if len(df_filtrado) == 0:
        print(f"⚠ No hay datos para el tipo de desastre: {tipo_desastre}")
        return fig

    # Gráfico 1: Distribución geográfica
    top_paises = df_filtrado['Country'].value_counts().head(10)
    top_paises.plot(kind='barh', ax=axes[0], color='coral')
    axes[0].set_title(f'Top 10 Países Afectados - {tipo_desastre}', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Cantidad de Eventos')
    axes[0].invert_yaxis()

    # Gráfico 2: Tendencia temporal
    if 'fecha' in df_filtrado.columns:
        temporal = df_filtrado.set_index('fecha').resample('Y').size()
        axes[1].plot(temporal.index, temporal.values, marker='o', linewidth=2, color='steelblue')
        axes[1].set_title(f'Tendencia Temporal - {tipo_desastre}', fontsize=12, fontweight='bold')
        axes[1].set_xlabel('Año')
        axes[1].set_ylabel('Cantidad de Eventos')
        axes[1].grid(True, alpha=0.3)

    # Gráfico 3: Impacto (muertes)
    if 'Total Deaths' in columnas_impacto and 'Total Deaths' in df_filtrado.columns:
        df_muertes = df_filtrado[df_filtrado['Total Deaths'] > 0]
        if len(df_muertes) > 0:
            top_mortales = df_muertes.nlargest(10, 'Total Deaths')[['Country', 'Total Deaths']]
            top_mortales.plot(x='Country', y='Total Deaths', kind='bar', ax=axes[2],
                            color='darkred', legend=False)
            axes[2].set_title(f'Top 10 Eventos más Mortales - {tipo_desastre}',
                            fontsize=12, fontweight='bold')
            axes[2].set_xlabel('País')
            axes[2].set_ylabel('Total de Muertes')
            axes[2].tick_params(axis='x', rotation=45, labelsize=9)

    # Gráfico 4: Estacionalidad
    if 'fecha' in df_filtrado.columns:
        df_filtrado['mes'] = df_filtrado['fecha'].dt.month
        estacional = df_filtrado['mes'].value_counts().sort_index()
        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        estacional.index = [meses[m-1] for m in estacional.index]

        axes[3].bar(range(len(estacional)), estacional.values, color='seagreen')
        axes[3].set_xticks(range(len(estacional)))
        axes[3].set_xticklabels(estacional.index)
        axes[3].set_title(f'Distribución Mensual - {tipo_desastre}', fontsize=12, fontweight='bold')
        axes[3].set_xlabel('Mes')
        axes[3].set_ylabel('Cantidad de Eventos')

    plt.tight_layout()
    return fig


def guardar_reporte(figuras, nombre_archivo='reporte_desastres.pdf'):
    """
    Guarda múltiples figuras en un archivo PDF

    Parámetros:
    -----------
    figuras : list
        Lista de figuras de matplotlib
    nombre_archivo : str
        Nombre del archivo PDF de salida
    """
    from matplotlib.backends.backend_pdf import PdfPages

    with PdfPages(nombre_archivo) as pdf:
        for fig in figuras:
            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)

    print(f"✓ Reporte guardado en: {nombre_archivo}")


def crear_visualizacion_cruces(df, tipo_cruce, columna_tipo='Disaster Type',
                               columna_pais='Country', columna_region='Region'):
    """
    Crea visualizaciones para cruces específicos de variables

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame con los datos
    tipo_cruce : str
        Tipo de cruce a analizar:
        - 'terremotos_geo': Distribución geográfica de terremotos
        - 'inundaciones_region': Regiones con mayor incidencia de inundaciones
        - 'sequias_region': Patrones regionales de sequías
        - 'tormentas_continente': Frecuencia de tormentas por continente
        - 'incendios_tendencia': Tendencia histórica de incendios forestales

    Retorna:
    --------
    matplotlib.figure.Figure
        Figura con la visualización
    """
    fig = plt.figure(figsize=(14, 8))

    if tipo_cruce == 'terremotos_geo':
        df_terremotos = df[df[columna_tipo].str.contains('Earthquake', case=False, na=False)]
        top_paises = df_terremotos[columna_pais].value_counts().head(15)

        ax = plt.subplot(111)
        top_paises.plot(kind='barh', ax=ax, color=plt.cm.Reds(np.linspace(0.4, 0.9, len(top_paises))))
        ax.set_title('Distribución Geográfica de Terremotos', fontsize=16, fontweight='bold')
        ax.set_xlabel('Cantidad de Terremotos', fontsize=12)
        ax.set_ylabel('País', fontsize=12)
        ax.invert_yaxis()

    elif tipo_cruce == 'inundaciones_region':
        df_inundaciones = df[df[columna_tipo].str.contains('Flood', case=False, na=False)]
        top_regiones = df_inundaciones[columna_region].value_counts().head(15)

        ax = plt.subplot(111)
        top_regiones.plot(kind='barh', ax=ax, color=plt.cm.Blues(np.linspace(0.4, 0.9, len(top_regiones))))
        ax.set_title('Regiones con Mayor Incidencia de Inundaciones', fontsize=16, fontweight='bold')
        ax.set_xlabel('Cantidad de Inundaciones', fontsize=12)
        ax.set_ylabel('Región', fontsize=12)
        ax.invert_yaxis()

    elif tipo_cruce == 'sequias_region':
        df_sequias = df[df[columna_tipo].str.contains('Drought', case=False, na=False)]
        top_regiones = df_sequias[columna_region].value_counts().head(15)

        ax = plt.subplot(111)
        top_regiones.plot(kind='barh', ax=ax, color=plt.cm.Oranges(np.linspace(0.4, 0.9, len(top_regiones))))
        ax.set_title('Patrones Regionales de Sequías Extremas', fontsize=16, fontweight='bold')
        ax.set_xlabel('Cantidad de Sequías', fontsize=12)
        ax.set_ylabel('Región', fontsize=12)
        ax.invert_yaxis()

    elif tipo_cruce == 'tormentas_continente':
        df_tormentas = df[df[columna_tipo].str.contains('Storm', case=False, na=False)]
        por_continente = df_tormentas['Continent'].value_counts()

        ax = plt.subplot(111)
        por_continente.plot(kind='bar', ax=ax, color=plt.cm.Purples(np.linspace(0.4, 0.9, len(por_continente))))
        ax.set_title('Frecuencia de Tormentas por Continente', fontsize=16, fontweight='bold')
        ax.set_xlabel('Continente', fontsize=12)
        ax.set_ylabel('Cantidad de Tormentas', fontsize=12)
        ax.tick_params(axis='x', rotation=45)

    elif tipo_cruce == 'incendios_tendencia':
        df_incendios = df[df[columna_tipo].str.contains('Wildfire', case=False, na=False)]

        if 'fecha' in df_incendios.columns and len(df_incendios) > 0:
            temporal = df_incendios.set_index('fecha').resample('Y').size()

            ax = plt.subplot(111)
            ax.plot(temporal.index, temporal.values, marker='o', linewidth=2.5,
                   color='darkorange', markersize=8)
            ax.fill_between(temporal.index, temporal.values, alpha=0.3, color='orange')
            ax.set_title('Tendencia Histórica de Incendios Forestales', fontsize=16, fontweight='bold')
            ax.set_xlabel('Año', fontsize=12)
            ax.set_ylabel('Cantidad de Incendios', fontsize=12)
            ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig
