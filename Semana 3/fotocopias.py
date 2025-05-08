#FOTOCOPIAS PARA APUNTES

import numpy as np

# Datos del problema
presupuesto = 8.0  # soles
precios = np.array([0.10, 0.12, 0.08])  # soles por página

# 1. Calcular cuántas páginas puede fotocopiar en cada copistería
paginas = np.floor(presupuesto / precios)
print("Páginas por copistería:", paginas)

# 2. Identificar la copistería con más páginas
mejor_opcion = np.argmax(paginas)
print("Copistería donde puede sacar más páginas:", mejor_opcion)
print("Número de páginas:", int(paginas[mejor_opcion]))

