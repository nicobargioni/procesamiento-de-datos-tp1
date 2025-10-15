#!/bin/bash

# Script de ejecución rápida del proyecto
# Uso: ./ejecutar.sh [opcion]
#   opcion: main (ejecuta main.py) o jupyter (abre notebook)

echo "========================================================================"
echo "PROYECTO DESASTRES NATURALES - ETL"
echo "========================================================================"

# Activar entorno virtual
source venv/bin/activate

# Verificar si se pasó un argumento
if [ "$1" = "jupyter" ]; then
    echo "Iniciando Jupyter Notebook..."
    jupyter notebook analisis_desastres_naturales.ipynb
elif [ "$1" = "main" ]; then
    echo "Ejecutando script principal..."
    python main.py
else
    echo ""
    echo "Opciones de ejecución:"
    echo "  1. ./ejecutar.sh main      - Ejecuta el script principal (main.py)"
    echo "  2. ./ejecutar.sh jupyter   - Abre el notebook de análisis"
    echo ""
    echo "Si no especificas opción, ejecutaré el script principal..."
    echo ""
    sleep 2
    python main.py
fi
