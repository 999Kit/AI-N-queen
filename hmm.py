import heapq

# Returns True if the given board state is valid (i.e., no two queens threaten each other)
def is_valid(board):
    for i in range(len(board)):
        for j in range(i+1, len(board)):
            if board[i] == board[j] or abs(board[i] - board[j]) == j - i:
                return False
    return True

# Computes the heuristic cost of the given board state as the number of attacking pairs of queens
def heuristic_cost(board):
    cost = 0
    for i in range(len(board)):
        for j in range(i+1, len(board)):
            if board[i] == board[j] or abs(board[i] - board[j]) == j - i:
                cost += 1
    return cost

# The A* algorithm
def solve():
    # The initial state is the empty board
    initial_state = tuple([None] * 8)

    # The priority queue for the A* algorithm
    priority_queue = []
    heapq.heappush(priority_queue, (heuristic_cost(initial_state), initial_state))

    # The reached table to store generated nodes
    reached = {initial_state: 0}

    while priority_queue:
        # Get the board state with the lowest total cost
        _, current_state = heapq.heappop(priority_queue)

        # If the board state is valid, return it
        if is_valid(current_state):
            return current_state

        # Generate all possible moves and add them to the priority queue
        for i in range(len(current_state)):
            for j in range(8):
                new_state = list(current_state)
                new_state[i] = j
                new_state = tuple(new_state)

                # Only add new states to the priority queue
                if new_state not in reached:
                    reached[new_state] = reached[current_state] + 1
                    heapq.heappush(priority_queue, (heuristic_cost(new_state) + reached[new_state], new_state))

    # If no valid board state was found, return None
    return None

# Print the solution
# print(solve())