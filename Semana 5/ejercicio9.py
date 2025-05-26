import numpy as np
import pandas as pd
from deap import base, creator, tools
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt
import random
from copy import deepcopy

# Cargar dataset
df = pd.read_csv("dataset/Emails.csv", sep=";")

# Separar características y etiqueta
X = df.iloc[:, :-1].values  # Features (Feature1 a Feature5)
y = df.iloc[:, -1].values   # Spam (0 o 1)

POP_SIZE = 20
N_GEN = 50
N_FEATURES = X.shape[1]

# Crear tipo fitness y individuo (maximizamos F1)
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Genera pesos y umbral entre [0,1]
toolbox.register("attr_float", random.uniform, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=N_FEATURES+1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def eval_individual(individual):
    pesos = np.array(individual[:-1])
    umbral = individual[-1]

    scores = X.dot(pesos)
    preds = (scores >= umbral).astype(int)

    f1 = f1_score(y, preds)
    return (f1,)

def mutate_and_hill_climb(individual, sigma=0.1, indpb=0.5, max_iter=10):
    best = deepcopy(individual)
    best.fitness.values = eval_individual(best)
    
    for _ in range(max_iter):
        mutant = deepcopy(best)
        for i in range(len(mutant)):
            if random.random() < indpb:
                mutant[i] += random.gauss(0, sigma)
                mutant[i] = min(max(mutant[i], 0), 1)  # limitar entre 0 y 1

        mutant.fitness.values = eval_individual(mutant)
        if mutant.fitness.values[0] > best.fitness.values[0]:
            best = mutant
    return best

toolbox.register("evaluate", eval_individual)
toolbox.register("mutate_hc", mutate_and_hill_climb)
toolbox.register("select", tools.selBest)

def main():
    pop = toolbox.population(n=POP_SIZE)

    for ind in pop:
        ind.fitness.values = toolbox.evaluate(ind)

    best_fitnesses = []
    best_individual = None
    best_score = 0

    for gen in range(N_GEN):
        offspring = []
        for ind in pop:
            mutant = toolbox.mutate_hc(ind)
            offspring.append(mutant)

        pop = toolbox.select(offspring, k=POP_SIZE)

        current_best = tools.selBest(pop, 1)[0]
        best_fitnesses.append(current_best.fitness.values[0])

        if current_best.fitness.values[0] > best_score:
            best_score = current_best.fitness.values[0]
            best_individual = deepcopy(current_best)

        print(f"Gen {gen}: Mejor F1 = {current_best.fitness.values[0]:.4f}")

    print("\nMejor individuo encontrado:")
    print(f"Pesos: {best_individual[:-1]}")
    print(f"Umbral: {best_individual[-1]:.4f}")
    print(f"F1-score: {best_score:.4f}")

    plt.plot(best_fitnesses)
    plt.xlabel("Generación")
    plt.ylabel("Mejor F1-score")
    plt.title("Curva de convergencia")
    plt.grid()
    plt.show()

if __name__ == "__main__":
    main()
