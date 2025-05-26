import pandas as pd
import random

# Leer el archivo CSV
df = pd.read_csv('dataset/Mentor.csv',delimiter=";")

# Mostrar las primeras filas para verificar los datos cargados
print(df.head())

# Extraemos los horarios de disponibilidad (0 = no disponible, 1 = disponible)
disponibilidad = df.values.tolist()

# Número de mentores (filas) y horarios (columnas)
num_mentores = len(disponibilidad)
num_horarios = len(disponibilidad[0])

# Función para calcular el costo (choques de horario)
def calcular_costo(horarios):
    choques = 0
    # Verificar cuántos choques hay entre los mentores
    for i in range(num_mentores):
        for j in range(i + 1, num_mentores):
            if horarios[i] == horarios[j]:  # Si dos mentores están asignados al mismo horario
                choques += 1
    return choques

# Función para generar un vecino (cambiar el horario de un mentor aleatorio)
def generar_vecino(horarios):
    vecino = horarios[:]
    mentor = random.randint(0, num_mentores - 1)
    # Seleccionar un horario aleatorio disponible para ese mentor
    horarios_disponibles = [col for col in range(num_horarios) if disponibilidad[mentor][col] == 1]
    nuevo_horario = random.choice(horarios_disponibles)
    vecino[mentor] = nuevo_horario
    return vecino

# Función Hill Climbing
def hill_climbing(iteraciones=1000):
    # Generar una solución inicial aleatoria
    horarios_iniciales = []
    for i in range(num_mentores):
        horarios_disponibles = [col for col in range(num_horarios) if disponibilidad[i][col] == 1]
        horario_aleatorio = random.choice(horarios_disponibles)
        horarios_iniciales.append(horario_aleatorio)
    
    costo_actual = calcular_costo(horarios_iniciales)
    
    for _ in range(iteraciones):
        # Generar un vecino
        vecino = generar_vecino(horarios_iniciales)
        costo_vecino = calcular_costo(vecino)
        
        # Si el vecino tiene un menor costo, lo aceptamos
        if costo_vecino < costo_actual:
            horarios_iniciales = vecino
            costo_actual = costo_vecino
        
        # Si encontramos una solución sin choques, podemos parar
        if costo_actual == 0:
            break
    
    return horarios_iniciales, costo_actual

# Ejecutar Hill Climbing
horarios_optimos, choques = hill_climbing(1000)

# Mostrar el resultado final
print("Asignación final de horarios:")
for i, horario in enumerate(horarios_optimos):
    print(f"Mentor {i + 1} tiene asignado el horario {horario + 1}")  # Sumamos 1 para mostrar el horario como un número de 1 a N

print(f"Total de choques: {choques}")
