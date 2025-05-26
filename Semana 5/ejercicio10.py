import numpy as np
import pandas as pd
import random
from copy import deepcopy
from deap import base, creator, tools
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score

# --- Carga y preparación de datos ---
df = pd.read_csv("dataset/Enrollments.csv", sep=";")

X = df.drop(columns=["Category"]).values.astype(float)
y_raw = df["Category"].values

le = LabelEncoder()
y = le.fit_transform(y_raw)

scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Parámetros para el genotipo ---
MIN_CAPAS = 1
MAX_CAPAS = 3
MIN_NEURONAS = 1
MAX_NEURONAS = 50
MIN_LR = 0.0001
MAX_LR = 0.1

# --- Crear tipos en DEAP ---
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

def init_individual():
    num_capas = random.randint(MIN_CAPAS, MAX_CAPAS)
    neuronas = [random.randint(MIN_NEURONAS, MAX_NEURONAS) if i < num_capas else 0 for i in range(MAX_CAPAS)]
    lr = random.uniform(MIN_LR, MAX_LR)
    return creator.Individual([num_capas] + neuronas + [lr])

toolbox.register("individual", init_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def build_model(individual):
    num_capas = individual[0]
    neuronas = individual[1:1+MAX_CAPAS]
    lr = individual[-1]

    model = Sequential()
    input_dim = X_train.shape[1]

    for i in range(num_capas):
        if i == 0:
            model.add(Dense(neuronas[i], input_dim=input_dim, activation='relu'))
        else:
            model.add(Dense(neuronas[i], activation='relu'))

    model.add(Dense(len(np.unique(y)), activation='softmax'))

    optimizer = Adam(learning_rate=lr)
    model.compile(loss='sparse_categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    return model

def eval_individual(individual):
    model = build_model(individual)
    model.fit(X_train, y_train, epochs=20, batch_size=16, verbose=0)
    loss, acc = model.evaluate(X_val, y_val, verbose=0)
    return (acc,)

def mutate_and_hill_climb(individual, sigma_lr=0.01, max_iter=5):
    best = deepcopy(individual)
    best.fitness.values = eval_individual(best)

    for _ in range(max_iter):
        mutant = deepcopy(best)

        if random.random() < 0.3:
            mutant[0] = random.randint(MIN_CAPAS, MAX_CAPAS)

        for i in range(1, 1 + MAX_CAPAS):
            if random.random() < 0.5:
                new_neurons = mutant[i] + random.choice([-1, 1])
                if i-1 >= mutant[0]:
                    mutant[i] = 0
                else:
                    mutant[i] = min(max(new_neurons, MIN_NEURONAS), MAX_NEURONAS)

        if random.random() < 0.5:
            mutant[-1] += random.gauss(0, sigma_lr)
            mutant[-1] = min(max(mutant[-1], MIN_LR), MAX_LR)

        mutant.fitness.values = eval_individual(mutant)

        if mutant.fitness.values[0] > best.fitness.values[0]:
            best = mutant

    return best

toolbox.register("evaluate", eval_individual)
toolbox.register("mutate_hc", mutate_and_hill_climb)
toolbox.register("select", tools.selBest)

def main():
    pop = toolbox.population(n=10)

    for ind in pop:
        ind.fitness.values = toolbox.evaluate(ind)

    best_individual = None
    best_score = 0
    fitness_history = []

    N_GEN = 15
    for gen in range(N_GEN):
        offspring = []
        for ind in pop:
            mutant = toolbox.mutate_hc(ind)
            offspring.append(mutant)

        pop = toolbox.select(offspring, k=len(pop))

        current_best = tools.selBest(pop, 1)[0]
        fitness_history.append(current_best.fitness.values[0])

        if current_best.fitness.values[0] > best_score:
            best_score = current_best.fitness.values[0]
            best_individual = deepcopy(current_best)

        print(f"Generación {gen}: Mejor accuracy = {current_best.fitness.values[0]:.4f}")

    print("\nMejor arquitectura encontrada:")
    print(f"Número de capas: {best_individual[0]}")
    print(f"Neuronas por capa: {best_individual[1:1+MAX_CAPAS]}")
    print(f"Tasa de aprendizaje: {best_individual[-1]:.5f}")
    print(f"Accuracy en validación: {best_score:.4f}")

if __name__ == "__main__":
    main()
