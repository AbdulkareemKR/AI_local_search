import numpy as np


def genetic_algorithm(population, m_rate=0.1, max_iters=5000):
    new_population = population
    best_state = population[0]
    num_iters = -1 # to skip the first iteration
    goal = False
    while num_iters < max_iters and not goal:
        population = new_population             # update old population
        probs = fitness_probs(new_population)   # calculate the probabilities of each state in the population
        max_index = np.argmax(np.array(probs))  # calculates tha maximum value index
        goal = is_goal(new_population[max_index])  # check if it is a goal state
        best_state = tuple(new_population[max_index])
        new_population = []

        for i in range(len(population)):
            parent1, parent2 = select_parents(population, probs)
            child = reproduce(parent1, parent2)
            mutated = mutate(child, m_rate)
            new_population.append(mutated)
        num_iters += 1
    return best_state, num_iters


def max_attacks(state):
    return (len(state) * (len(state) - 1)) / 2  # finding the highest number of possible attacks in N*N queens

def fitness_sum(population):
    fitnesses = []
    for state in population:  # iterate over the initial populating to find fitness for each one of them
        fitnesses.append(fitness(state))
    return [fitnesses, sum(fitnesses)]  # save the sum of all fitnesses

def fitness(state):  # Returns the fitness value of a state
    real_attacks = 0
    for q1 in range(len(state) - 1):  # iterate till before the last element
        for q2 in range(q1 + 1, len(state)):  # from q1 + 1 up to the last queen
            if state[q1] == state[q2] or q2 - q1 == abs(
                    state[q1] - state[q2]):  # if they are in the same row or in the same diagonal
                real_attacks += 1
    fitness_value = max_attacks(state) - real_attacks
    return fitness_value


def is_goal(state):  # Returns true if the given state is the goal solution
    return fitness(state) == max_attacks(state)


def fitness_probs(population):  # Returns a list of probabilities for the states in the population.
    probabilities, sum = fitness_sum(population)
    for i in range(len(probabilities)):
        probabilities[i] /= sum  # updating probabilities to percentage instead of values
    return tuple(probabilities)


def select_parents(population, probs): # Returns a single state that is the result of reproducing 2 parents.
    parent = np.random.choice(len(population), 2, True, probs)  # arg1 is an array or int arg2 number of selected items arg3 with repeating arg4 the probabilities of each choice
    return population[parent[0]], population[parent[1]]  # return the tuples at the parent indices


def reproduce(parent1, parent2):
    state_size = len(parent1)
    crossover_point = np.random.randint(state_size, high=None, size=1,
                                        dtype=int)  # return a single random list element (int) from 0 to state size
    child = list(parent1)
    for i in range(crossover_point[0], state_size):  # generating a crossovered child from the two parents
        child[i] = parent2[i]
    return tuple(child)


def mutate(state, m_rate=0.1):
    sample_float = np.random.uniform(low=0, high=1,size=1)  # return a single random double list element between 0 and less than 1
    mutated = list(state)
    if sample_float <= m_rate:  # if the sample float is less than m_rate, then we mutate
        first_sample = np.random.randint(len(state), high=None, size=1, dtype=int)
        second_sample = np.random.randint(len(state), high=None, size=1, dtype=int)
        mutated[first_sample[0]] = second_sample[0]
    return mutated

def