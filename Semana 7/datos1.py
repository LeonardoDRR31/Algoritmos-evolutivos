import pandas as pd
import plotly.express as px

# Mostrar todas las columnas sin cortar
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Leer el archivo CSV
df = pd.read_csv("notas_1u.csv")
# Declarar e imprimir las estadísticas general
moda = df['Nota'].mode()[0]        # Moda
media = df['Nota'].mean()          # Media
mediana = df['Nota'].median()      # Mediana
desviacion = df['Nota'].std()      # Desviación estándar
varianza = df['Nota'].var() 
print ("=============================================================================")
print(f"Moda: {moda}")
print(f"Media: {media}")
print(f"Mediana: {mediana}")
print(f"Desviación estándar: {desviacion}")
print(f"Varianza: {varianza}")
print ("=============================================================================") 
# Estadísticas por tipo de examen
stats = df.groupby("Tipo_Examen")["Nota"].agg(
    count='count',
    mean='mean',
    median='median',
    mode=lambda x: x.mode().iloc[0] if not x.mode().empty else None,
    std='std',
    var='var',
    min='min',
    max='max',
    rango=lambda x: x.max() - x.min()
).sort_values(by="mean", ascending=False)

# Mostrar estadísticas
print("📊 Estadísticas por tipo de examen:")
print(stats)

# Determinar cuál examen fue el más fácil (mayor promedio)
tipo_mas_facil = stats["mean"].idxmax()
print(f"\n🏆 El tipo de examen con mejor promedio fue: {tipo_mas_facil}")

# Gráfico interactivo: Boxplot
fig_box = px.box(df, x="Tipo_Examen", y="Nota", color="Tipo_Examen",
                 title="Distribución de Notas por Tipo de Examen (Boxplot)",
                 labels={"Nota": "Nota", "Tipo_Examen": "Tipo de Examen"})
fig_box.update_layout(boxmode='group')
fig_box.show()

# Gráfico interactivo: Violin plot
fig_violin = px.violin(df, x="Tipo_Examen", y="Nota", color="Tipo_Examen", box=True, points="all",
                       title="Distribución de Notas por Tipo de Examen (Violin Plot)",
                       labels={"Nota": "Nota", "Tipo_Examen": "Tipo de Examen"})
fig_violin.show()
