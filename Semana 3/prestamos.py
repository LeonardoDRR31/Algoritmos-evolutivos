#PRESTAMO DE LIBROS EN LA BIBLIOTECA
import pandas as pd
import matplotlib.pyplot as plt
# Datos del préstamo
datos = {
    'Nombre': ['Rosa', 'David', 'Elena', 'Mario', 'Paula'],
    'Días_prestamo': [7, 10, 5, 12, 8]
}
df = pd.DataFrame(datos)

# Mostrar el DataFrame
print("Datos del préstamo de libros:")
print(df)

# Calcular promedio, máximo y resumen estadístico
resumen = df['Días_prestamo'].describe()
print("\nResumen estadístico:")
print(resumen)

promedio = resumen['mean']
maximo = resumen['max']
print(f"\nPromedio de días: {promedio:.2f}")
print(f"Máximo de días: {int(maximo)}")

# Filtrar quienes retuvieron el libro más de 8 días
mas_de_8_dias = df[df['Días_prestamo'] > 8]
print("\nCompañeros que retuvieron el libro más de 8 días:")
print(mas_de_8_dias)

# Calcular promedio, máximo y resumen estadístico
resumen = df['Días_prestamo'].describe()
promedio = resumen['mean']
maximo = resumen['max']

# Crear la tabla usando matplotlib
fig, ax = plt.subplots(figsize=(6, 4))  # Tamaño de la figura

# Ocultar los ejes
ax.axis('tight')
ax.axis('off')

# Crear tabla
tabla = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center', colColours=['#f5f5f5']*len(df.columns))

# Añadir texto de resumen debajo de la tabla
tabla.auto_set_font_size(False)
tabla.set_fontsize(10)

# Añadir texto de resumen
ax.text(0.5, -0.1, f'Promedio de días: {promedio:.2f}', ha='center', va='center', fontsize=12)
ax.text(0.5, -0.15, f'Máximo de días: {int(maximo)}', ha='center', va='center', fontsize=12)

plt.show()

