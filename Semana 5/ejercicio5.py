import pandas as pd
import random
from collections import defaultdict

# Leer el archivo CSV
df = pd.read_csv('dataset/Tesistas.csv',delimiter=";")

# Mostrar las primeras filas para verificar los datos cargados
print(df.head())

# Extraemos los datos del CSV
tesistas = df['TesistaID'].tolist()  # Cambiar 'Tesistas' a 'TesistaID'
salas = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6']  # Salas disponibles
franjas = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8']  # Franjas horarias disponibles

# Inicialización de la asignación de tesistas a salas y franjas
# Codificamos la solución como un diccionario {tesista: (sala, franja)}
asignacion_inicial = {}
for i, tesista in enumerate(tesistas):
    sala = salas[i % len(salas)]  # Asignación secuencial de salas
    franja = franjas[i % len(franjas)]  # Asignación secuencial de franjas
    asignacion_inicial[tesista] = (sala, franja)

# Función para calcular los huecos y solapamientos
def calcular_metricas(asignacion):
    solapamientos = 0
    huecos = defaultdict(int)

    # Verificar solapamientos
    franjas_por_sala = defaultdict(list)
    for tesista, (sala, franja) in asignacion.items():
        franjas_por_sala[sala].append(franja)

    for sala, franjas_asignadas in franjas_por_sala.items():
        franjas_asignadas.sort()  # Ordenamos las franjas
        for i in range(1, len(franjas_asignadas)):
            if franjas_asignadas[i] == franjas_asignadas[i-1]:  # Si hay solapamiento
                solapamientos += 1
        
        # Verificar huecos (falta de franjas en la sala)
        huecos[sala] = len(franjas) - len(set(franjas_asignadas))  # Número de franjas faltantes

    return solapamientos, huecos

# Función para generar un vecino (mover 1 tesista a otra franja/sala)
def generar_vecino(asignacion):
    tesista = random.choice(tesistas)
    nueva_sala = random.choice(salas)
    nueva_franja = random.choice(franjas)
    asignacion_vecino = asignacion.copy()
    asignacion_vecino[tesista] = (nueva_sala, nueva_franja)
    return asignacion_vecino

# Función Hill Climbing
def hill_climbing(iteraciones=1000):
    asignacion_actual = asignacion_inicial
    solapamientos_actual, huecos_actual = calcular_metricas(asignacion_actual)
    
    for _ in range(iteraciones):
        vecino = generar_vecino(asignacion_actual)
        solapamientos_vecino, huecos_vecino = calcular_metricas(vecino)
        
        # Si el vecino mejora la solución (menos solapamientos y/o huecos)
        if solapamientos_vecino < solapamientos_actual or \
           (solapamientos_vecino == solapamientos_actual and sum(huecos_vecino.values()) < sum(huecos_actual.values())):
            asignacion_actual = vecino
            solapamientos_actual = solapamientos_vecino
            huecos_actual = huecos_vecino
    
    return asignacion_actual, solapamientos_actual, huecos_actual

# Ejecutar Hill Climbing
asignacion_optima, solapamientos_optimos, huecos_optimos = hill_climbing(1000)

# Mostrar el resultado final
print("Asignación final de tesistas:")
for tesista, (sala, franja) in asignacion_optima.items():
    print(f"{tesista}: {sala} - {franja}")

print(f"\nSolapamientos: {solapamientos_optimos}")
print(f"Huecos: {huecos_optimos}")
