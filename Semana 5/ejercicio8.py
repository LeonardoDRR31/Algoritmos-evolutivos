import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

from deap import base, creator, tools

# Parámetros DEAP
POP_SIZE = 20
N_GEN = 50  # generaciones
ALPHA_BOUNDS = (0.0001, 10)
R_BOUNDS = (50, 500)  # ejemplo para max_iter

# 1. Cargar dataset
df = pd.read_csv("dataset/HousePrices.csv",sep=";")

# Supongo que 'Price' es la variable objetivo, ajustar si es otro nombre
X = df.drop(columns=["Price_Soles"])
y = df["Price_Soles"].values

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Crear función evaluación
def eval_ridge(individual):
    alpha, max_iter = individual
    max_iter = int(max_iter)
    model = Ridge(alpha=alpha, max_iter=max_iter, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    return (rmse,)

# 3. Setup DEAP
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # Minimizar RMSE
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Indivíduo: [alpha, max_iter]
toolbox.register("attr_alpha", np.random.uniform, *ALPHA_BOUNDS)
toolbox.register("attr_max_iter", np.random.uniform, *R_BOUNDS)
toolbox.register("individual", tools.initCycle, creator.Individual,
                 (toolbox.attr_alpha, toolbox.attr_max_iter), n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Evaluación
toolbox.register("evaluate", eval_ridge)

# Mutación: gaussiana pequeña, sin cruce
def mutate_individual(individual, mu, sigma, indpb):
    for i in range(len(individual)):
        if np.random.rand() < indpb:
            individual[i] += np.random.normal(mu, sigma)
            # Limitar al rango
            if i == 0:  # alpha
                individual[i] = min(max(individual[i], ALPHA_BOUNDS[0]), ALPHA_BOUNDS[1])
            else:  # max_iter
                individual[i] = int(min(max(individual[i], R_BOUNDS[0]), R_BOUNDS[1]))
    return individual,

toolbox.register("mutate", mutate_individual, mu=0, sigma=0.1, indpb=0.5)

# Selección greedy: seleccionar el mejor individuo entre población y vecinos mutados
def select_greedy(pop, offspring):
    combined = pop + offspring
    combined.sort(key=lambda ind: ind.fitness.values)
    return combined[:len(pop)]

toolbox.register("select", select_greedy)

# 4. Algoritmo hill climbing con población
def main():
    pop = toolbox.population(n=POP_SIZE)

    # Evaluar inicial
    for ind in pop:
        ind.fitness.values = toolbox.evaluate(ind)

    best_fit_vals = []
    for gen in range(N_GEN):
        offspring = []
        for ind in pop:
            mutant, = toolbox.mutate(toolbox.clone(ind))
            mutant.fitness.values = toolbox.evaluate(mutant)
            offspring.append(mutant)

        pop = toolbox.select(pop, offspring)
        best = tools.selBest(pop, 1)[0]
        best_fit_vals.append(best.fitness.values[0])
        print(f"Gen {gen}: Mejor RMSE={best.fitness.values[0]:.4f}, α={best[0]:.4f}, max_iter={int(best[1])}")

    # Plot convergencia
    import matplotlib.pyplot as plt
    plt.plot(best_fit_vals)
    plt.xlabel("Generación")
    plt.ylabel("Mejor RMSE")
    plt.title("Curva de convergencia")
    plt.grid()
    plt.show()

    best = tools.selBest(pop, 1)[0]
    print(f"\nMejor individuo final: α={best[0]:.4f}, max_iter={int(best[1])}, RMSE={best.fitness.values[0]:.4f}")

if __name__ == "__main__":
    main()
