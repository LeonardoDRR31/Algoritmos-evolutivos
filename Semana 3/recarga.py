#RECARGA DE DATOS MÓVILES
import numpy as np

# Datos de los paquetes
gb = np.array([1, 2, 5, 10])         # Gigabytes por paquete
precios = np.array([5, 9, 20, 35])   # Precio en soles

# 1. Calcular el costo por GB
costo_por_gb = precios / gb
print("Costo por GB para cada paquete:", costo_por_gb)

# 2. Encontrar el paquete más económico en precio por GB
min_costo = costo_por_gb.min()
mejor_paquete = costo_por_gb.argmin()
print("Paquete más económico por GB: índice", mejor_paquete)
print(f"GB: {gb[mejor_paquete]}, Precio: S/ {precios[mejor_paquete]}")
print(f"Costo por GB: S/ {min_costo:.2f}")
