##AJUSTE DE HORARIOS DE ESTUDIO
import numpy as np
import random
import math

# Materias
materias = ['Mate', 'Química', 'Historia', 'Lengua', 'Física']

# Simulamos una matriz de fatiga entre materias
np.random.seed(0)  # Reproducible
fatiga = np.random.randint(1, 6, size=(5, 5))
np.fill_diagonal(fatiga, 0)  # Cero fatiga al no cambiar de materia

# Función para calcular el costo total de una secuencia
def calcular_costo(secuencia, matriz_fatiga):
    return sum(matriz_fatiga[secuencia[i], secuencia[i+1]] for i in range(len(secuencia) - 1))

# Mapeamos materias a índices (0–4)
materia_indices = list(range(5))
secuencia_actual = materia_indices[:]
mejor_secuencia = secuencia_actual[:]
mejor_costo = calcular_costo(secuencia_actual, fatiga)

# Simulated Annealing
T_inicial = 10
T_final = 1
iteraciones = 100

for paso in range(iteraciones):
    T = T_inicial - (T_inicial - T_final) * (paso / iteraciones)

    # Generar vecino: intercambiar dos materias al azar
    vecino = secuencia_actual[:]
    i, j = random.sample(range(5), 2)
    vecino[i], vecino[j] = vecino[j], vecino[i]

    costo_actual = calcular_costo(secuencia_actual, fatiga)
    costo_vecino = calcular_costo(vecino, fatiga)
    delta = costo_vecino - costo_actual

    if delta < 0 or random.random() < math.exp(-delta / T):
        secuencia_actual = vecino[:]
        if costo_vecino < mejor_costo:
            mejor_secuencia = vecino[:]
            mejor_costo = costo_vecino

# Mostrar resultados
materias_finales = [materias[i] for i in mejor_secuencia]
print("Mejor secuencia encontrada:", materias_finales)
print("Costo total de fatiga:", mejor_costo)
