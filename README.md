# Semana 7

Este directorio contiene una serie de archivos relacionados con análisis de datos y aprendizaje automático, desarrollados como parte de la Semana 7 del curso.

## 📁 Contenido del directorio

### `datos1.py`
Contiene un algoritmo que extrae **estadísticas básicas** a partir de un conjunto de datos guardado en el archivo `notas_1u.csv`.  
El script realiza operaciones como cálculo de promedios, máximos, mínimos y otros análisis descriptivos.

---

### `datos2.py`
Implementa un **modelo de aprendizaje automático simple**.  
Utiliza datos reales y ficticios generados a partir del script `dataset.py`.  
Pasos que realiza:
- Carga el archivo `notas_estu.csv`
- Divide los datos en un **80% para entrenamiento** y **20% para prueba**
- Entrena un modelo para **predecir si un estudiante aprobará el curso**, basándose en variables como nota, asistencia, participación, etc.

---

### `dataset.py`
Generador de datos aleatorios basados en variables específicas.  
Este script toma como referencia los datos de `notas_1u.csv` para crear datasets simulados que luego son usados por `datos2.py`.

---

### `notas_1u.csv`
Archivo `.csv` que contiene un conjunto de datos reales o simulados de estudiantes, utilizado por `datos1.py` y `dataset.py`.

---

### `notas_estu.csv`
Archivo `.csv` que contiene datos preprocesados y generados para alimentar el modelo de aprendizaje automático en `datos2.py`.

---

## 🧠 Propósito general

Estos scripts permiten practicar:
- Lectura y análisis de archivos CSV con Python
- Generación de datasets sintéticos
- Entrenamiento y evaluación de modelos de clasificación simples
