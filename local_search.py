import numpy as np


def fitness(state):  # Returns the fitness value of a state
    max_attacks = (len(state) * (len(state) - 1)) / 2  # finding the highest number of possible attacks in N*N queens
    real_attacks = 0

    for q1 in range(len(state) - 1):  # iterate till before the last element
        for q2 in range(q1 + 1, len(state)):  # from q1 + 1 up to the last queen
            if state[q1] == state[q2] or q2 - q1 == abs(
                    state[q1] - state[q2]):  # if they are in the same row or in the same diagonal
                real_attacks += 1
    fitness_value = max_attacks - real_attacks
    return fitness_value


def is_goal(state):  # Returns true if the given state is the goal solution
    max_attacks = (len(state) * (len(state) - 1)) / 2
    return fitness(state) == max_attacks


def fitness_probs(population):  # Returns a list of probabilities for the states in the population.
    probabilities = []
    for state in population:  # iterate over the initial populating to find fitness for each one of them
        probabilities.append(fitness(state))
    fitness_sum = sum(probabilities)  # save the sum of all fitnesses 
    for i in range(len(probabilities)):
        probabilities[i] /= fitness_sum  # updating probabilities to percentage instead of values
    return probabilities


def select_parents(population, probs):
    parent = np.random.choice(len(population), 2, True,
                              probs)  # arg1 is an array or int arg2 number of selected items arg3 with repeating arg4 the probabilities of each choice
    return [population[parent[0]], population[parent[1]]]  # return the tuples at the parent indices


def reproduce(parent1, parent2):
    state_size = len(parent1)
    crossover_point = np.random.randint(state_size, high=None, size=1,
                                        dtype=int)  # return a single random list element (int) from 0 to state size
    child = list(parent1)
    for i in range(crossover_point[0], state_size):  # generating a crossovered child from the two parents
        child[i] = parent2[i]
    return tuple(child)


def mutate(state, m_rate=0.1):
    sample_float = np.random.uniform(low=0, high=1,
                                     size=1)  # return a single random double list element between 0 and less than 1
    if sample_float <= m_rate:
