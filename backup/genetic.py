from random import choices, randint, uniform
from math import comb
from numpy import random
import tracemalloc

import time

State = list[int] # a genetic representation of a solution
Population = list[State]

print ("Enter the number of queens")
N = int(input())

Mutation_rate: float = 80
# Population_size: int = 2*N*N
Population_size: int = 100
Queen_pairs = comb(N, 2)
Generation_limit = int

class h_s:
    def __init__(self, h: int, state: list):
        self.h = h
        self.state = state
    def __lt__(self, other):
        return self.h < other.h


def generate_state() -> State:
    state = list(range(0, N))
    for _ in range(N):
        pos1 = randint(0, N-1)
        pos2 = randint(0, N-1)
        state[pos1], state[pos2] = state[pos2], state[pos1]
    return state

# a function to generate new solutions
# def generate_population(size: int) -> Population: 
#     return [generate_state() for _ in range(size)]

def generate_h_pop(size: int) -> h_s: 
    h_pop = [h_s]
    for _ in range(size):
        state = generate_state()
        h_pop.append(h_s(fitness(state), state))
    return h_pop

# a fitness function to evaluate solutions
def fitness(state: State) -> int:
    row = [0] * N
    main_diag = [0]*(N*2 - 1)
    sub_diag = [0]*(N*2 - 1)

    h = 0
    for col in range(N):
        h += row[state[col]]
        h += main_diag[state[col] - col - 1 + N]
        h += sub_diag[state[col] + col]

        row[state[col]] += 1
        main_diag[state[col] - col - 1 + N] += 1
        sub_diag[state[col] + col] += 1
    return h

# a selection function to select parents to generate a solution
def parent_selection(p: Population) -> list[State, State]:
    fit_sum = int(sum(h for h, _ in p))
    roulette = [fit/fit_sum for fit,_ in p]
    ind1, ind2 = random.choice(Population_size, 2, p = roulette)

    return [p[ind1], p[ind2]]


def mutation(state: State) -> State:
    pos1 = randint(0, N-1)
    pos2 = randint(0, N-1)
    state[pos1], state[pos2] = state[pos2], state[pos1]
    return state


# def crossover(a: State, b: State) -> list[State, State]:
#     if len(a) < 2:
#         return a, b

#     c = randint(1, len(a)-1)
#     return a[0:c]+ b[c:], b[0:c] + a[c:]

def pmx_crossover(parent1, parent2):

    cross1 = randint(0, N-2)
    cross2 = randint(cross1+1, N-1)

    child1 = list(parent1)
    child2 = list(parent2)

    for i in range(cross1, cross2+1):
        if child1[i] != parent2[i]:
            pos1 = child1.index(parent2[i])
            child1[i], child1[pos1] = child1[pos1], child1[i]

        if child2[i] != parent1[i]:
            pos2 = child2.index(parent1[i])
            child2[i], child2[pos2] = child2[pos2], child2[i]
    return child1, child2


def genetic_algorithm() -> State:
    global population
    gen = 2
    elitism_size = int(Population_size/10)
    # if elitism_size % 2 == 1:
    #     elitism_size += 1
    while gen:
        population.sort()
        f = fitness(population[0].h)
        
        # done
        if f == 0:
            print("Generation: ", gen)
            return population[0].state
        population = population[:Population_size]
        if gen % 1000 == 0:
            print(gen, f)
        gen += 1

        population2 = population[0:elitism_size]

        # for i in range(int(Population_size/2) - int(elitism_size/2)):
        for i in range(int(Population_size/2)):
            parent1, parent2 = parent_selection(population)
            # child1, child2 = crossover(parent1, parent2)
            child1, child2 = pmx_crossover(parent1, parent2)
            # if choices([1, 0], weights=[Mutation_rate, 1 - Mutation_rate], k = 1)[0]:
            if randint(0,99) <= Mutation_rate:
                child1 = mutation(child1)
            if randint(0,99) <= Mutation_rate:
            # if choices([1, 0], weights=[Mutation_rate, 1 - Mutation_rate], k = 1)[0]:
                child2 = mutation(child2)
            population2 += [child1, child2]
            
        population = population2
    return []


# population = generate_population(Population_size)
population = generate_h_pop(Population_size)
# print(population)

kkk = [None]*10
print(len(kkk))

print("GA")
print("N = ", N)

tracemalloc.start()
start_time = time.time()

# genetic_algorithm()

run_time = (time.time() - start_time)*1000
memory = tracemalloc.get_traced_memory()

print("Running time(ms): ", run_time)
print("Memory(MB): ", memory)
