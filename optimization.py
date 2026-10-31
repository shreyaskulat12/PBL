
import random
import math

# Objective Function
def objective(x):
    return (x - 7) ** 2


# Hill Climbing Algorithm
def hill_climbing():

    current = 0

    while True:

        neighbors = [current - 1, current + 1]

        best = min(neighbors, key=objective)

        if objective(best) < objective(current):
            current = best
        else:
            break

    return current


# Simulated Annealing Algorithm
def simulated_annealing():

    random.seed(42)

    current = 0
    best = current

    temperature = 100
    cooling_rate = 0.95

    while temperature > 0.1:

        neighbor = current + random.choice([-1, 1])

        change = objective(neighbor) - objective(current)

        if change < 0:
            current = neighbor

        else:
            probability = math.exp(-change / temperature)

            if random.random() < probability:
                current = neighbor

        if objective(current) < objective(best):
            best = current

        temperature *= cooling_rate

    return best


# Main Program
print("Hill Climbing Algorithm")

hc = hill_climbing()

print("Best Solution:", hc)
print("Minimum Value:", objective(hc))

print("\nSimulated Annealing Algorithm")

sa = simulated_annealing()

print("Best Solution:", sa)
print("Minimum Value:", objective(sa))
