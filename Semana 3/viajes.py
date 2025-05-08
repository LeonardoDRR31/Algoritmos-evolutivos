#VIAJE AL CAMPUS
import numpy as np

# Datos del problema
presupuesto = 15.0  # soles disponibles
precios = np.array([2.50, 3.00, 1.80])  # precios de bus, combi y tren

# 1. Calcular cuántos viajes puede pagar con cada medio
viajes = np.floor(presupuesto / precios)
print("Viajes por medio de transporte:", viajes)

# 2. Hallar el medio que permite más viajes
max_viajes = viajes.max()
mejor_opcion = viajes.argmax()
print("Medio de transporte con más viajes:", mejor_opcion)
print("Cantidad de viajes:", int(max_viajes))
