import numpy as np


def fitness(state):
    max_attacks = (len(state) * (len(state) - 1)) / 2  # finding the highest number of possible attacks in N*N queens
    real_attacks = 0

    for q1 in range(len(state) - 1):  # iterate till before the last element
        for q2 in range(q1 + 1, len(state)):  # from q1 + 1 up to the last queen
            if state[q1] == state[q2] or q2 - q1 == abs(
                    state[q1] - state[q2]):  # if they are in the same row or in the same diagonal
                real_attacks += 1
    fitness_value = max_attacks - real_attacks
    return fitness_value


def is_goal(state):
    max_attacks = (len(state) * (len(state) - 1)) / 2
    return fitness(state) == max_attacks




