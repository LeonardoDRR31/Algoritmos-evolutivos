#Una pequeña empresa produce dos tipos de artesanías: A y B.
#	Escenario A requiere 2 horas de trabajo y da S/. 50 de ganancia.
#	Escenario B requiere 3 horas de trabajo y da S/. 80 de ganancia.
#Se dispone de un máximo de 120 horas de trabajo por semana.
#Se deben producir al menos 10 unidades de A y 5 de B.
#	Objetivo: Maximizar la ganancia semanal
#Tarea: 1. Identifiquen en papel o documento:
	#Variables de decisión (¿Qué decide la empresa?).
	#Función objetivo (¿Qué quiere maximizar? Escriban la fórmula)
	#Restricciones (¿Que limitaciones tiene? Escríbanlas)
#Variables de decisión
#	x: número de unidades del producto A a producir por semana
#	y: número de unidades del producto B a producir por semana

#Función objetivo
    #Maximizar→Z=50x+80y
# Restricciones de horas de trabajo
    #2x+3y≤120
# Restricciones de producción mínima
    #x≥10
# No negatividad
    #x≥0 ;y≥0 
# Resumen del modelo de programación lineal
    #       2x+3y ≤ 120
    #       x     ≥
    #       y     ≥
    #       z ≥ 0 y y ≥ 0
import numpy as np
import plotly.graph_objects as go
from scipy.optimize import linprog
import webbrowser
import os

# --- Resolver el modelo ---
c = [-50, -80]  # Max Z = 50x + 80y → Min -50x -80y
A = [[2, 3]]
b = [120]
x_bounds = (10, None)
y_bounds = (5, None)

res = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method='highs')

# --- Datos para graficar ---
x = np.linspace(0, 80, 400)
y1 = (120 - 2 * x) / 3
y1 = np.where(y1 < 0, 0, y1)

# Zona factible: solo donde x >= 10 y y >= 5 y 2x + 3y <= 120
x_f = []
y_f = []
for xi, yi in zip(x, y1):
    if xi >= 10 and yi >= 5:
        x_f.append(xi)
        y_f.append(yi)

# Cierra la región para graficar
x_f += [80, 10]
y_f += [5, 5]

# --- Gráfico interactivo ---
fig = go.Figure()

# Zona factible
fig.add_trace(go.Scatter(
    x=x_f,
    y=y_f,
    fill='toself',
    fillcolor='rgba(144,238,144,0.4)',
    line=dict(color='green'),
    name='Zona factible'
))

# Restricción: 2x + 3y <= 120
fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name='2x + 3y ≤ 120', line=dict(color='blue')))

# Restricciones x ≥ 10 y y ≥ 5
fig.add_trace(go.Scatter(x=[10,10], y=[0,60], mode='lines', name='x ≥ 10', line=dict(dash='dash', color='red')))
fig.add_trace(go.Scatter(x=[0,80], y=[5,5], mode='lines', name='y ≥ 5', line=dict(dash='dash', color='orange')))

# Solución óptima
if res.success:
    x_opt, y_opt = res.x
    z_opt = -res.fun
    fig.add_trace(go.Scatter(
        x=[x_opt],
        y=[y_opt],
        mode='markers+text',
        name='Solución óptima',
        marker=dict(color='black', size=10),
        text=[f'Óptimo: ({x_opt:.1f}, {y_opt:.1f})<br>Z = S/. {z_opt:.2f}'],
        textposition='top right'
    ))

# Layout
fig.update_layout(
    title='Optimización de Ganancias - Artesanías A y B',
    xaxis_title='Cantidad de A (x)',
    yaxis_title='Cantidad de B (y)',
    showlegend=True
)

# Mostrar gráfico en el navegador
file_path = 'grafico_optimizacion.html'
fig.write_html(file_path, auto_open=True)

