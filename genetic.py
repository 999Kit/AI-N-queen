from random import choices, randint

import time

State = list[int] # a genetic representation of a solution
Population = list[State]

def generate_state(length: int) -> State:
    return choices([0, 1], k=length)

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
    return h

# a selection function to select parents to generate a solution
def parent_selection(population: Population) -> list[State, State]:
    return choices(
        population=population,
        weights=[fitness(state) for state in population],
        k=2
    )

def crossover(a: State, b: State) -> list[State, State]:
    c = randint(1, len(a)-1)
    


State = generate_state(N)
print (State)

# def genetic_algorithm(population, fitness) -> genome:
    