import pandas as pd
import numpy as np
import random

# Leer el archivo CSV usando el delimitador correcto ";"
df = pd.read_csv('dataset/LabDistances.csv', sep=';', index_col=0)

# Verifica que los datos se leyeron correctamente
print(df)

# Convertir el DataFrame a una matriz de NumPy, solo con los valores numéricos
dist_matrix = df.to_numpy()

# Verificar la matriz de distancias
print(dist_matrix)

def calcular_distancia(ruta, dist_matrix):
    distancia_total = 0
    for i in range(len(ruta) - 1):
        distancia_total += dist_matrix[ruta[i], ruta[i+1]]
    # Añadir la distancia de regreso al punto de inicio
    distancia_total += dist_matrix[ruta[-1], ruta[0]]
    return distancia_total

def generar_vecindad(ruta):
    # Intercambiar dos nodos aleatorios
    i, j = random.sample(range(len(ruta)), 2)
    ruta_vecina = ruta[:]
    ruta_vecina[i], ruta_vecina[j] = ruta_vecina[j], ruta_vecina[i]
    return ruta_vecina

def hill_climbing(dist_matrix, iteraciones=1000):
    # Generar una ruta inicial aleatoria
    ruta_actual = list(range(len(dist_matrix)))
    random.shuffle(ruta_actual)
    
    distancia_actual = calcular_distancia(ruta_actual, dist_matrix)
    
    for _ in range(iteraciones):
        # Generar una vecindad
        vecindad = generar_vecindad(ruta_actual)
        distancia_vecindad = calcular_distancia(vecindad, dist_matrix)
        
        # Si la vecindad tiene una mejor solución, aceptar el cambio
        if distancia_vecindad < distancia_actual:
            ruta_actual = vecindad
            distancia_actual = distancia_vecindad
    
    return ruta_actual, distancia_actual

# Ejecutar Hill Climbing
ruta_optima, distancia_optima = hill_climbing(dist_matrix, 1000)

# Mostrar el resultado
print(f'Orden óptimo de los laboratorios: {ruta_optima}')
print(f'Distancia total recorrida: {distancia_optima} metros')
