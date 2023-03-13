import heapq
import time

print ("Enter the number of queens")
N = int(input())


# N = None
# initial_state = [0] * N
initial_state = tuple([0] * N) # so it can be used as a dictionary key


def print_board(state):
    board = [[0]*N for _ in range(N)] 
    for col in range(N):
        board[state[col]][col] = 1
    for cell in board:
        print(cell)

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



class Node:
    def __init__(self, state, g, h):
        self.state = state
        self.g_cost = g
        self.h_cost = h

    def __lt__(self, other):
        return self.g_cost+self.h_cost < other.g_cost + other.h_cost



# def A_star():
#     root = Node(initial_state, 0, evaluate_heuristic(initial_state))
#     reached = {} # dictionary
#     pq = [] # implemented using list

#     reached[root.state] = 0
#     heapq.heappush(pq, root)
    
#     while pq:
#         node = heapq.heappop(pq)

#         if node.h_cost == 0:
#             return node
#         for col in range(N):
#             for row in range(N):
#                 new_state = list(node.state)
#                 new_state[col] = row
#                 new_state = tuple(new_state)
#                 if new_state not in reached or node.g_cost+1 < reached[new_state]:
#                     child = Node(new_state, node.g_cost+ 1, evaluate_heuristic(new_state))
#                     reached[new_state] = child.g_cost
#                     heapq.heappush(pq, child)
    
#     return None

def A_star():
    root = Node(initial_state, 0, evaluate_heuristic(initial_state))
    reached = {} # dictionary
    pq = [] # implemented using list

    reached[root.state] = 0
    heapq.heappush(pq, root)
    
    while pq:
        node = heapq.heappop(pq)

        if node.h_cost == 0:
            return node
        for col in range(N):
            for row in range(N):
                new_state = list(node.state)
                new_state[col] = row
                new_state = tuple(new_state)
                if new_state not in reached:
                    child = Node(new_state, 0, evaluate_heuristic(new_state))
                    reached[new_state] = 0
                    heapq.heappush(pq, child)
    return None

# def UCS():
#     root = Node(initial_state, 0, 0)
#     reached = {} # dictionary
#     pq = [] # implemented using list

#     reached[root.state] = 0
#     heapq.heappush(pq, root)
    
#     while pq:
#         node = heapq.heappop(pq)

#         for col in range(N):
#             for row in range(N):
#                 new_state = list(node.state)
#                 new_state[col] = row
#                 new_state = tuple(new_state)
#                 if evaluate_heuristic(new_state) == 0: 
#                     return Node(new_state, node.g_cost+1, 0)
#                 if new_state not in reached or node.g_cost+1 < reached[new_state]:
#                     # print(new_state)
#                     child = Node(new_state, node.g_cost+ 1, 0)
#                     reached[new_state] = child.g_cost
#                     heapq.heappush(pq, child)
    
#     return None

def UCS():
    # root = Node(initial_state, 0, 0)
    reached = {} # dictionary
    pq = [] # implemented using list

    # reached[root.state] = 0
    reached[initial_state] = 1
    # heapq.heappush(pq, root)
    pq.append(initial_state)
    
    while pq:
        # node = heapq.heappop(pq)
        cur = pq.pop(0)

        for col in range(N):
            for row in range(N):
                new_state = list(cur)
                new_state[col] = row
                new_state = tuple(new_state)
                if evaluate_heuristic(new_state) == 0: 
                    return Node(new_state, 0, 0)
                if new_state not in reached:
                    # print(new_state)
                    # child = Node(new_state, 0, 0)
                    reached[new_state] = 1
                    # heapq.heappush(pq, child)
                    pq.append(new_state)
    
    return None

start_time = time.time()
# goal = A_star()
goal = UCS()
print((time.time() - start_time)*1000)

# print(goal)
if goal:
    print(goal.state)
else:
    print("Can't")
# print_board(goal.state)
# print(evaluate_heuristic(initial_state))

# def main():
#     print ("Enter the number of queens")
#     N = int(input())
#     goal = A_star(initial_state)
#     print_board(goal)





