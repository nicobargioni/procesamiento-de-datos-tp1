# 🚀 Inicio Rápido - Proyecto Desastres Naturales

## ✅ Entorno Virtual Creado

El entorno virtual ya está configurado y las dependencias instaladas.

---

## 📋 Cómo Usar el Proyecto

### Opción 1: Script de Ejecución Rápida (Más Fácil)

```bash
# Ejecutar el análisis completo
./ejecutar.sh

# O específicamente el notebook
./ejecutar.sh jupyter

# O el script principal
./ejecutar.sh main
```

### Opción 2: Ejecución Manual

#### 1. Activar el entorno virtual:
```bash
source venv/bin/activate
```

#### 2. Ejecutar el proyecto:

**Opción A - Script principal:**
```bash
python main.py
```

**Opción B - Jupyter Notebook (Recomendado):**
```bash
jupyter notebook analisis_desastres_naturales.ipynb
```

#### 3. Desactivar el entorno cuando termines:
```bash
deactivate
```

---

## 📦 Dependencias Instaladas

✅ pandas 2.3.3
✅ numpy 2.3.4
✅ matplotlib 3.10.7
✅ seaborn 0.13.2
✅ jupyter 1.1.1

---

## 📁 Estructura del Proyecto

```
proyecto_desastres_naturales/
├── venv/                    ← Entorno virtual (ya configurado)
├── extract/                 ← Módulo de extracción
├── transform/               ← Módulo de transformación
├── load/                    ← Módulo de visualización
├── main.py                  ← Script principal
├── analisis_desastres_naturales.ipynb  ← Notebook completo
├── ejecutar.sh              ← Script de ejecución rápida
└── README.md                ← Documentación completa
```

---

## ⚠️ Importante

Antes de ejecutar, verifica que el dataset esté en la ubicación correcta:
```
../1970-2021_DISASTERS.xlsx - emdat data.csv
```

Si está en otro lugar, actualiza la ruta en:
- `main.py` (línea 146)
- `analisis_desastres_naturales.ipynb` (celda de carga)

---

## 🎯 ¿Qué hace cada componente?

### `main.py`
Ejecuta el proceso ETL completo:
1. Extrae y valida los datos
2. Transforma y limpia el dataset
3. Genera visualizaciones
4. Muestra resumen estadístico

### `analisis_desastres_naturales.ipynb`
Notebook interactivo con:
- Análisis exploratorio completo
- Visualizaciones detalladas
- Apreciaciones críticas
- Interpretaciones y conclusiones
- Los 5 cruces de variables requeridos

---

## 💡 Consejos

1. **Primera vez**: Usa el notebook para ver todo el análisis paso a paso
2. **Ejecuciones rápidas**: Usa `./ejecutar.sh main`
3. **Para la entrega**: El notebook es más completo y tiene todas las interpretaciones

---

## 🔧 Solución de Problemas

### Error: "command not found: jupyter"
```bash
source venv/bin/activate
pip install jupyter
```

### Error: "No such file or directory: dataset"
- Verifica la ruta del dataset en `main.py` y el notebook

### El entorno no se activa
```bash
# Verificar que existe
ls venv/

# Recrear si es necesario
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## ✨ Todo Listo!

Tu entorno está configurado y listo para usar. Ejecuta:

```bash
./ejecutar.sh jupyter
```

Para comenzar con el análisis completo.
