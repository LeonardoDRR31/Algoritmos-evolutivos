import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Mostrar todas las columnas sin cortar
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Leer el archivo CSV
df = pd.read_csv("notas_1u.csv")
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
print ("_____________________________________________________________________________")
print(stats)
# Determinar cuál examen fue el más fácil (mayor promedio)
tipo_mas_facil = stats["mean"].idxmax()
print(f"\n🏆 El tipo de examen con mejor promedio fue: {tipo_mas_facil}")
print ("=============================================================================")
# Gráfico de caja (Boxplot)
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="Tipo_Examen", y="Nota", hue="Tipo_Examen", palette="pastel", legend=False)
plt.title("Distribución de Notas por Tipo de Examen (Boxplot)")
plt.xlabel("Tipo de Examen")
plt.ylabel("Nota")
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# Gráfico de violín (Violin plot)
plt.figure(figsize=(8, 5))
sns.violinplot(data=df, x="Tipo_Examen", y="Nota", hue="Tipo_Examen", palette="Set2", legend=False)
plt.title("Distribución de Notas por Tipo de Examen (Violin Plot)")
plt.xlabel("Tipo de Examen")
plt.ylabel("Nota")
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
