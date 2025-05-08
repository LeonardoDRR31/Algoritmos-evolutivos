#GATOS DE ALMUERZO SEMANAL
import pandas as pd

# Lista de gastos de lunes a viernes
gastos = [4.0, 3.5, 5.0, 4.2, 3.8]
dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']

# 1. Crear el DataFrame
df = pd.DataFrame({'Día': dias, 'Gasto': gastos})

# 2. Calcular el gasto total y el gasto promedio
gasto_total = df['Gasto'].sum()
gasto_promedio = df['Gasto'].mean()

print("Gasto total de la semana: S/", gasto_total)
print("Gasto promedio diario: S/", round(gasto_promedio, 2))

# 3. Días donde gastó más que el promedio
dias_mayores = df[df['Gasto'] > gasto_promedio]
print("\nDías con gasto mayor al promedio:")
print(dias_mayores)
