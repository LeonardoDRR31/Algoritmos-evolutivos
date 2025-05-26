import pandas as pd
# Ajustar para mostrar todas las filas y columnas
pd.set_option('display.max_rows', None)  # Muestra todas las filas
pd.set_option('display.max_columns', None)
# Leer el archivo CSV
df = pd.read_csv('dataset/Grades.csv',delimiter=";")

# Mostrar las primeras filas para verificar los datos
print(df.head(10))
def funcion_aptitud(df, offset):
    # Aplicar el offset a las calificaciones
    df_offset = df[['Parcial1', 'Parcial2', 'Parcial3']] + offset

    # Calcular el promedio por estudiante
    df['Promedio'] = df_offset.mean(axis=1)
    
    # Contar los aprobados (promedio >= 10)
    aprobados = (df['Promedio'] >= 10).sum()

    # Calcular el porcentaje de aprobados
    porcentaje_aprobados = aprobados / len(df) * 100
    
    # Penalizar si el promedio de la clase > 14
    promedio_clase = df['Promedio'].mean()
    penalizacion = 0
    if promedio_clase > 14:
        penalizacion = (promedio_clase - 14) * 10  # Penalización lineal

    # La aptitud es el porcentaje de aprobados menos la penalización
    aptitud = porcentaje_aprobados - penalizacion
    return aptitud, df
import random

def hill_climbing(df):
    # Inicializar un offset aleatorio entre -5 y +5
    offset = random.uniform(-5, 5)
    mejor_offset = offset
    mejor_aptitud, df_mejor = funcion_aptitud(df, offset)

    # Definir los límites de iteración
    iteraciones = 1000  # Número de iteraciones de hill climbing
    paso = 0.5  # El paso del offset

    for _ in range(iteraciones):
        # Generar un nuevo offset aleatorio dentro de un rango pequeño alrededor del actual
        nuevo_offset = offset + random.uniform(-paso, paso)

        # Evitar que el nuevo offset se salga del rango permitido
        nuevo_offset = max(-5, min(5, nuevo_offset))

        # Calcular la aptitud para el nuevo offset
        aptitud, df_nuevo = funcion_aptitud(df, nuevo_offset)

        # Si la nueva aptitud es mejor, actualizar el mejor offset
        if aptitud > mejor_aptitud:
            mejor_aptitud = aptitud
            mejor_offset = nuevo_offset
            df_mejor = df_nuevo

        # Actualizar el offset actual
        offset = nuevo_offset

    return mejor_offset, df_mejor
# Ejecutar Hill Climbing
mejor_offset, df_mejor = hill_climbing(df)

# Mostrar el offset óptimo y la nueva distribución de calificaciones
print(f"Offset óptimo encontrado: {mejor_offset}")
print(df_mejor[['StudentID', 'Parcial1', 'Parcial2', 'Parcial3', 'Promedio']])
