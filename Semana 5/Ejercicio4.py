import pandas as pd
import random

# Leer el archivo CSV para obtener los proyectos, costos y beneficios
df = pd.read_csv('dataset/projects.csv',delimiter=";")
print(df.columns)

# Extraer los costos y beneficios de las columnas correspondientes
costos = df['Cost_Soles'].tolist()  # Columna de costos
beneficios = df['Benefit_Soles'].tolist()  # Columna de beneficios
presupuesto_maximo = 10000  # Presupuesto máximo

# Función de aptitud: Si el costo total está dentro del presupuesto, devuelve el beneficio total; de lo contrario, -∞
def funcion_aptitud(bitstring):
    costo_total = sum(costo for i, costo in enumerate(costos) if bitstring[i] == 1)
    if costo_total <= presupuesto_maximo:
        beneficio_total = sum(beneficio for i, beneficio in enumerate(beneficios) if bitstring[i] == 1)
        return beneficio_total
    else:
        return float('-inf')  # Penalizar si el costo total excede el presupuesto

# Función para generar un vecino (voltear un bit aleatorio)
def generar_vecindad(bitstring):
    vecino = bitstring[:]
    i = random.randint(0, len(bitstring) - 1)
    vecino[i] = 1 - vecino[i]  # Voltear el bit en la posición i
    return vecino

# Algoritmo de Hill Climbing
def hill_climbing(iteraciones=1000):
    # Generar una solución inicial aleatoria
    bitstring_actual = [random.randint(0, 1) for _ in range(len(costos))]
    beneficio_actual = funcion_aptitud(bitstring_actual)
    
    for _ in range(iteraciones):
        # Generar un vecino
        vecino = generar_vecindad(bitstring_actual)
        beneficio_vecino = funcion_aptitud(vecino)
        
        # Si el vecino tiene una mejor aptitud, aceptarlo
        if beneficio_vecino > beneficio_actual:
            bitstring_actual = vecino
            beneficio_actual = beneficio_vecino
    
    return bitstring_actual, beneficio_actual

# Ejecutar Hill Climbing
bitstring_optimo, beneficio_optimo = hill_climbing(1000)

# Mostrar el resultado
proyectos_seleccionados = [i + 1 for i in range(len(bitstring_optimo)) if bitstring_optimo[i] == 1]

print(f'Proyectos seleccionados: {proyectos_seleccionados}')
print(f'Beneficio total: S/ {beneficio_optimo}')
