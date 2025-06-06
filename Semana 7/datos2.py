import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import plotly.express as px
import plotly.graph_objects as go

# Cargar el dataset
df = pd.read_csv('notas_estu.csv')

# Separar variable objetivo (Nota) y las características predictoras
X = df.drop(columns=['Alumno', 'Nota'])
y = df['Nota']

# Codificar variables categóricas como dummies
X_encoded = pd.get_dummies(X, drop_first=True)

# Dividir en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.2, random_state=42
)

# Entrenar modelo de regresión lineal
model = LinearRegression()
model.fit(X_train, y_train)

# Predicción
y_pred = model.predict(X_test)

# Evaluación del modelo
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"✅ Evaluación del Modelo:")
print(f" - Error cuadrático medio (MSE): {mse:.3f}")
print(f" - R² score: {r2:.3f}")

# Mostrar coeficientes
coef_df = pd.DataFrame({
    'Feature': X_encoded.columns,
    'Coeficiente': model.coef_
}).sort_values(by='Coeficiente', ascending=False)

print("\n📊 Coeficientes del modelo:")
print(coef_df)

# Gráfico 1: Notas reales vs predichas
df_compare = pd.DataFrame({
    'Nota Real': y_test,
    'Nota Predicha': y_pred
}).reset_index(drop=True)

fig1 = px.scatter(df_compare, x='Nota Real', y='Nota Predicha',
                  title='Notas Reales vs Notas Predichas',
                  trendline='ols', width=700, height=500)
fig1.update_traces(marker=dict(size=10, color='blue'))
fig1.show()

# Gráfico 2: Importancia de variables (coeficientes)
fig2 = go.Figure(go.Bar(
    x=coef_df['Coeficiente'],
    y=coef_df['Feature'],
    orientation='h',
    marker=dict(color='green')
))
fig2.update_layout(title='Importancia de Variables (Coeficientes del Modelo)',
                   xaxis_title='Coeficiente',
                   yaxis_title='Variable',
                   yaxis={'categoryorder':'total ascending'})
fig2.show()
