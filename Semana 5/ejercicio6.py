import pandas as pd
import random

# Leer el archivo CSV
df = pd.read_csv('dataset/ExamQuestions.csv',delimiter=";")

# Mostrar las primeras filas para verificar los datos cargados
print(df.head())

# Extraemos los datos del CSV
dificultades = df['Difficulty'].tolist()  # Dificultad de las preguntas
tiempos = df['Time_min'].tolist()  # Tiempo estimado en minutos de cada pregunta

# Parámetros del examen
max_dificultad = 200
min_dificultad = 180
max_tiempo = 90

# Función para calcular el costo (aptitud) de una solución
def calcular_costo(bitstring):
    dificultad_total = 0
    tiempo_total = 0
    for i, bit in enumerate(bitstring):
        if bit == 1:
            dificultad_total += dificultades[i]
            tiempo_total += tiempos[i]
    
    # Penalización si el tiempo excede el máximo permitido o la dificultad no está en el rango permitido
    if tiempo_total > max_tiempo:
        return -float('inf')  # Penaliza si se excede el tiempo
    if dificultad_total < min_dificultad or dificultad_total > max_dificultad:
        return -float('inf')  # Penaliza si la dificultad no está en el rango [180, 200]
    
    return dificultad_total  # El costo es la dificultad total si es válida

# Función para generar un vecino (cambiar un bit aleatorio en el bitstring)
def generar_vecino(bitstring):
    vecino = bitstring.copy()
    i = random.randint(0, len(bitstring) - 1)
    vecino[i] = 1 - vecino[i]  # Cambiar el valor del bit (de 0 a 1 o de 1 a 0)
    return vecino

# Función Hill Climbing
def hill_climbing(iteraciones=1000):
    # Generar una solución inicial aleatoria
    bitstring_inicial = [random.randint(0, 1) for _ in range(len(dificultades))]
    costo_actual = calcular_costo(bitstring_inicial)
    
    for _ in range(iteraciones):
        vecino = generar_vecino(bitstring_inicial)
        costo_vecino = calcular_costo(vecino)
        
        # Si el vecino es mejor que la solución actual, lo aceptamos
        if costo_vecino > costo_actual:
            bitstring_inicial = vecino
            costo_actual = costo_vecino
    
    return bitstring_inicial, costo_actual

# Ejecutar Hill Climbing
bitstring_optimo, costo_optimo = hill_climbing(1000)

# Mostrar el resultado final
print("Bitstring óptimo de selección de preguntas:")
print(bitstring_optimo)
print(f"Dificultad total: {costo_optimo}")
print(f"Tiempo total: {sum([tiempos[i] for i, bit in enumerate(bitstring_optimo) if bit == 1])} minutos")
