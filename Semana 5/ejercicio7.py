import pandas as pd
import numpy as np
import random
from copy import deepcopy

# Parámetros
N_EQUIPOS = 3
TAM_EQUIPO = 5
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

# 1. Cargar datos (usa ; como separador)
df = pd.read_csv("dataset/Students.csv", sep=";")

# 2. Normalizar nombres de columnas
df.columns = df.columns.str.strip()

# 3. Transformar Skill en one-hot
df_onehot = pd.get_dummies(df, columns=["Skill"])
gpas = df_onehot["GPA"].values
habilidades = df_onehot.drop(columns=["StudentID", "GPA"]).values
alumnos = df_onehot.index.tolist()
n_habilidades = habilidades.shape[1]

# 4. Generar equipos aleatorios
def generar_equipos():
    indices = alumnos.copy()
    random.shuffle(indices)
    return [indices[i * TAM_EQUIPO:(i + 1) * TAM_EQUIPO] for i in range(N_EQUIPOS)]

# 5. Calcular fitness
def calcular_fitness(equipos):
    varianzas_gpa = []
    distribuciones = np.zeros((N_EQUIPOS, n_habilidades))

    for i, equipo in enumerate(equipos):
        gpa_equipo = gpas[equipo]
        varianzas_gpa.append(np.mean(gpa_equipo))
        distribuciones[i] = habilidades[equipo].sum(axis=0)

    varianza_gpa = np.var(varianzas_gpa)
    ideal = distribuciones.mean(axis=0)
    penalizacion = np.sum((distribuciones - ideal) ** 2)
    return varianza_gpa + penalizacion

# 6. Generar vecino
def generar_vecino(equipos):
    nuevo = deepcopy(equipos)
    eq1, eq2 = random.sample(range(N_EQUIPOS), 2)
    i1 = random.randint(0, TAM_EQUIPO - 1)
    i2 = random.randint(0, TAM_EQUIPO - 1)
    nuevo[eq1][i1], nuevo[eq2][i2] = nuevo[eq2][i2], nuevo[eq1][i1]
    return nuevo

# 7. Búsqueda local
def optimizar(iteraciones=1000):
    actual = generar_equipos()
    mejor_fitness = calcular_fitness(actual)

    for _ in range(iteraciones):
        vecino = generar_vecino(actual)
        fitness_vecino = calcular_fitness(vecino)

        if fitness_vecino < mejor_fitness:
            actual = vecino
            mejor_fitness = fitness_vecino

    return actual, mejor_fitness

# 8. Ejecutar
equipos_finales, fitness_final = optimizar(2000)

# 9. Mostrar resultados
for i, equipo in enumerate(equipos_finales):
    print(f"Equipo {i+1}: {[df.loc[e, 'StudentID'] for e in equipo]}")
    print(f"  GPA promedio: {np.mean(gpas[equipo]):.2f}")
    print(f"  Habilidades: {habilidades[equipo].sum(axis=0)}\n")

print(f"Fitness final: {fitness_final:.4f}")
