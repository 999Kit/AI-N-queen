from random import choices
import time

print ("Enter the number of queens")
N = int(input())

initial_state = tuple([0] * N) # so it can be used as a dictionary key

def evaluate_heuristic(state):
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


genome = list[int] 
population = list[genome]

def generate_genome(length: int) -> genome:
    return choices([0, 1], k=length)

def generate_population(size: int, genome_length: int) -> population:
    return [generate_genome(genome_length)]

genome = generate_genome(N)
print (genome)

# def genetic_algorithm(population, fitness) -> genome:
    