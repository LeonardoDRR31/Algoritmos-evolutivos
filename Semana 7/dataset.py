import pandas as pd
import numpy as np
from io import StringIO

# Datos originales
data = """
Alumno,Nota,Tipo_Examen
Alumno1,15.0,C
Alumno2,13.0,C
Alumno3,14.0,C
Alumno4,10.0,A
Alumno5,15.0,C
Alumno6,11.0,C
Alumno7,14.0,C
Alumno8,13.0,C
Alumno9,13.0,A
Alumno10,17.0,C
Alumno11,19.0,B
Alumno12,19.0,A
Alumno13,14.0,A
Alumno14,17.0,A
Alumno15,19.0,B
Alumno16,16.0,A
Alumno17,20.0,C
Alumno18,16.0,A
Alumno19,20.0,B
Alumno20,19.0,B
Alumno21,13.0,B
Alumno22,20.0,B
Alumno23,16.0,A
Alumno24,11.0,A
Alumno25,18.0,C
Alumno26,19.0,B
Alumno27,18.0,B
Alumno28,13.0,B
Alumno29,14.0,A
Alumno30,20.0,B
Alumno31,19.0,B
Alumno32,18.0,C
Alumno33,18.0,B
Alumno34,9.0,C
Alumno35,11.0,C
Alumno36,14.0,A
Alumno37,13.0,A
Alumno38,9.0,B
Alumno39,14.0,A
"""

# Leer los datos originales
df = pd.read_csv(StringIO(data))

# Fijar semilla para reproducibilidad
np.random.seed(42)

# Generar Edad (entre 21 y 24)
df['Edad'] = np.random.randint(21, 25, size=len(df))

# Generar Horas de estudio (entre 2 y 4), con decimales
df['Horas_Estudio'] = np.round(np.random.uniform(2, 4, size=len(df)), 1)

# Generar Horas de dedicación a la materia (entre 1 y 3), con decimales
df['Horas_Dedicacion'] = np.round(np.random.uniform(1, 3, size=len(df)), 1)

# Generar Género (95% Masculino, 5% Femenino)
df['Genero'] = np.random.choice(['Masculino', 'Femenino'], size=len(df), p=[0.95, 0.05])

# Definir función para asignar dificultad según Nota y Tipo_Examen
def asignar_dificultad(row):
    # Regla ficticia para dificultad:
    # Tipo A o Nota < 13 -> Alta
    # Tipo B -> Media
    # Tipo C -> Baja
    if row['Tipo_Examen'] == 'A' or row['Nota'] < 13:
        return 'Alta'
    elif row['Tipo_Examen'] == 'B':
        return 'Media'
    else:
        return 'Baja'

df['Dificultad'] = df.apply(asignar_dificultad, axis=1)

# Guardar CSV con nuevos datos
df.to_csv('notas_estudiantes_completo.csv', index=False)

print("Archivo 'notas_estudiantes_completo.csv' generado con éxito.")
print(df.head())
df.to_csv('notas_estudiantes_completo.csv', index=False)
print("Archivo CSV generado exitosamente.")