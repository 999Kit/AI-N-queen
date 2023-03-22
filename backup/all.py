import heapq
import time
import tracemalloc

from random import choices, randint
from math import comb

# State = tuple[int]

N = int
initial_state = tuple

def generate_state() -> tuple:
    return choices(list(range(0,N)), k=N)

def count_attacking(state: tuple) -> int:
    main_diag = {}
    sub_diag = {}
    row = {}

    h = 0
    for col in range(N):
        main_diag_key = state[col] - col - 1 + N
        sub_diag_key = state[col] + col
        row_key = state[col]

        h += main_diag.get(main_diag_key, 0)
        h += sub_diag.get(sub_diag_key, 0)
        h += row.get(row_key, 0)

        main_diag[main_diag_key] = main_diag.get(main_diag_key, 0) + 1
        sub_diag[sub_diag_key] = sub_diag.get(sub_diag_key, 0) + 1
        row[row_key] = row.get(row_key, 0) + 1
    return h


def UCS(initial_state):
    root = ([0, initial_state])
    reached = {} # dictionary
    pq = [] # priority implemented using list

    reached[root[1]] = 0
    heapq.heappush(pq, root)
    
    while pq:
        node = heapq.heappop(pq)

        if count_attacking(node[1]) == 0:
            return node[1]
        for col in range(N):
            for row in range(N):
                if row == node[1][col]:
                    continue
                new_state = list(node[1])
                new_state[col] = row
                new_state = tuple(new_state)
                new_g = node[0]+1
                if new_state not in reached or new_g < reached[new_state]:     
                    child = (new_g, new_state)
                    reached[new_state] = new_g
                    heapq.heappush(pq, child)
    return []

def A_star(initial_state):
    root_h = count_attacking(initial_state)
    root = ([root_h + 0, initial_state, 0])
    reached = {} # dictionary
    pq = [] # implemented using list

    reached[root[1]] = (0, root_h)
    heapq.heappush(pq, root)
    
    while pq:
        node = heapq.heappop(pq)

        if node[0] - node[2] == 0:
            return node[1]
        for col in range(N):
            for row in range(N):
                if row == node[1][col]:
                    continue
                new_state = list(node[1])
                new_state[col] = row
                new_state = tuple(new_state)
                new_g = node[2]+1
                if new_state not in reached or new_g < reached[new_state][0]:     
                    if new_state in reached:
                        h = reached[new_state][1]
                    else:
                        h = count_attacking(new_state)
                    child = (new_g+h, new_state, new_g)
                    reached[new_state] = [new_g, h]
                    heapq.heappush(pq, child)
    return []


def generate_chromo() -> list:
    state = list(range(0, N))
    for _ in range(N):
        pos1 = randint(0, N-1)
        pos2 = randint(0, N-1)
        state[pos1], state[pos2] = state[pos2], state[pos1]
    return state

def generate_population(size: int) -> list: 
    pop = []
    for _ in range(size):
        state = generate_chromo()
        pop.append((fitness(state), state))
    return pop

def fitness(state: list) -> int:
    main_diag = {}
    sub_diag = {}

    h = 0
    for col in range(N):
        main_diag_key = state[col] - col - 1 + N
        sub_diag_key = state[col] + col

        h += main_diag.get(main_diag_key, 0)
        h += sub_diag.get(sub_diag_key, 0)

        main_diag[main_diag_key] = main_diag.get(main_diag_key, 0) + 1
        sub_diag[sub_diag_key] = sub_diag.get(sub_diag_key, 0) + 1
    return 1.0/(h+1)

# a selection function to select parents to generate a solution
def parent_selection(population: list) -> list:
    parent1, parent2 = choices(
        population=population,
        weights=[fit for fit,_ in population],
        k=2
    )
    return parent1[1], parent2[1]


def mutation(state: list) -> list:
    pos1 = randint(0, N-1)
    pos2 = randint(0, N-1)
    state[pos1], state[pos2] = state[pos2], state[pos1]
    return state

def pmx_crossover(parent1, parent2):
    cross1 = randint(0, N-2)
    cross2 = randint(cross1+1, N-1)

    child1 = parent1
    child2 = parent2

    for i in range(cross1, cross2+1):
        if child1[i] != parent2[i]:
            pos1 = child1.index(parent2[i])
            child1[i], child1[pos1] = child1[pos1], child1[i]

        if child2[i] != parent1[i]:
            pos2 = child2.index(parent1[i])
            child2[i], child2[pos2] = child2[pos2], child2[i]
    return child1, child2


def genetic_algorithm():
    global population
    gen = 1
    elitism_size = int(Population_size/10)

    while gen:
        population.sort(reverse = True)
        fit = population[0][0]
        
        # goal_test
        if fit == 1:
            print("Generation: ", gen)
            return population[0][1]

        gen += 1

        population2 = population[0:elitism_size]

        for i in range(int((Population_size-elitism_size)/2)):
            parent1, parent2 = parent_selection(population)

            child1, child2 = pmx_crossover(parent1, parent2)
            if randint(1,100) <= Mutation_rate:
                child1 = mutation(child1)
            if randint(1,100) <= Mutation_rate:
                child2 = mutation(child2)

            population2.append((fitness(child1), child1))
            population2.append((fitness(child2), child2))

        population = population2
    return []
    

Population_size = 100
Generation_limit = 10000
Mutation_rate = 20

Queen_pairs = int
population = []


def print_board(state: tuple):
    board = [[0]*N for _ in range(N)] 
    for col in range(N):
        board[state[col]][col] = 1
    for cell in board:
        print(cell)

def run():
    global N
    global initial_state
    global Queen_pairs
    global population
    N = 0
    while 1:

        while N == 0:
            print ("Enter the number of queens (-1 to exit.)")
            N = int(input())
            if N == -1:
                return
            elif N < 1:
                print("The number of queens is at least 1! Please input again.") 
            elif N > 500:
                print("Input is too large!")

        while 1:
            print("0. Back")
            print("1. Uniform-cost search.")
            print("2. A*")
            print("3. Genetic algorithm")

            c = int(input())
            if c < 0 or c > 3:
                print("Invalid input!")
                continue
            elif c == 0:
                break

            initial_state = tuple(generate_state())
            Queen_pairs = N*(N-1)/2
            algo_name = ""
            initial_population = generate_population(Population_size)

            start_time = time.time()
            tracemalloc.start()
            if c == 1:
                goal_state = UCS(initial_state)
                algo_name = "Uniform-cost search algorithm"
            elif c == 2:
                goal_state = A_star(initial_state)
                algo_name = "A* algorithm"
            else:
                goal_state = genetic_algorithm()
                algo_name = "Genetic algorithm"
            run_time = (time.time() - start_time)*1000
            memory = tracemalloc.get_traced_memory()

            print(algo_name)
            if N <= 10:
                print("The chess board after:") 
                print_board(goal_state)
            else:
                print("The state after (chess board too large)")
                print(goal_state)
            print("Running time (ms): ", run_time)
            print("Memory (MB): ", memory)


run()