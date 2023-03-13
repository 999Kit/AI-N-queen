from random import choices, randint
from math import comb

import time

State = list[int] # a genetic representation of a solution
Population = list[State]


# N = 8
print ("Enter the number of queens")
N = int(input())

Mutation_rate: float = 0.01
Population_size: int = 4

def generate_state(length: int) -> State:
    return choices(list(range(0,N)), k=length)

# a function to generate new solutions
def generate_population(size: int, state_length: int) -> Population: 
    return [generate_state(state_length) for _ in range(size)]

# a fitness function to evaluate solutions
def fitness(state: State) -> int:
    N = len(state)
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
    return comb(N, 2) - h

# a selection function to select parents to generate a solution
def parent_selection(population: Population) -> list[State, State]:
    return choices(
        population=population,
        weights=[fitness(state) for state in population],
        k=2
    )

def crossover(a: State, b: State) -> list[State, State]:
    if len(a) < 2:
        return a, b

    c = randint(1, len(a)-1)
    return a[0:c]+ b[c:], b[0:c] + a[c:]

def mutation(state: State) -> State:
    for index in range(0, len(state)):
        flip = choices([1, 0], weights=[Mutation_rate, 1 - Mutation_rate], k = 1)[0]
        if flip == 1:
            state[index] = choices(list(range(0,N)), k=1)[0]
    return state



# c = randint(1, 5)

# a = [0,1,1,0,1,0,0,0]
# a+=[99, 97]
# print(a)
# print(mutation(a))
# print(Mutation_rate, 1- Mutation_rate)
# population = generate_population(Population_size,8)

# parent1, parent2 = parent_selection(population)
# print(parent1, parent2)


# num: int = 1
# for _ in range(num):
#     print("hi")
# print(a)
# print (a[1:5])

# State = generate_state(N)
# print (State)

def genetic_algorithm() -> State:
    population = generate_population(Population_size,N)
    print(population)

    while 1:
    # for i in range(2):
        for state in population:
            if fitness(state) == 0:
                print(state)
                return state
        population2: Population = []
        for i in range(int(Population_size/2)):
            parent1, parent2 = parent_selection(population)
            # print(fitness(parent1), fitness(parent2))
            child1, child2 = crossover(parent1, parent2)
            if choices([1, 0], weights=[Mutation_rate, 1 - Mutation_rate], k = 1)[0]:
                mutation(child1)
            if choices([1, 0], weights=[Mutation_rate, 1 - Mutation_rate], k = 1)[0]:
                mutation(child2)
            population2 += [child1, child2]
        population = population2
        # print(population)
            
    return []


# print(fitness(population[0]))
print(genetic_algorithm())
