from queue import PriorityQueue
from time import time

class State:

    DIRECTIONS = ['←', '→', '↑', '↓']
    def __init__(self, state, parent, direction, depth, cost, goal):
        self.state = state
        self.parent = parent
        self.direction = direction
        self.depth = depth
        self.goal = goal

        if parent:
            self.cost = parent.cost + cost
        else:
            self.cost = cost

    def has_letters(self):
        for item in self.state:
            if isinstance(item, str) and item.isalpha():
                return True
        return False

    def is_goal(self):
        return self.state == self.goal

    def manhattan_distance(self, n):
        self.heuristic = 0
        for i in range(1, n * n):
            distance = abs(self.state.index(i) - self.goal.index(i))
            self.heuristic = self.heuristic + distance // n + distance % n

        self.a_star_evaluation = self.heuristic + self.cost
        return self.a_star_evaluation

    def manhattan_modified(self, n):
        self.heuristic = 0
        for i in range(1, 9):
            if i!= 'a':
                distance = abs(i - (i-1)//n) + abs((i-1)%n - (i-1)//n)
                self.heuristic += distance
        self.AStar_evaluation = self.heuristic + self.cost
        return self.AStar_evaluation


    @staticmethod
    def available_moves(x, n):
        moves = State.DIRECTIONS.copy()
        if x % n == 0:
            moves.remove('←') #Left
        if x % n == n - 1:
            moves.remove('→') #Right
        if x - n < 0:
            moves.remove('↑') #Up
        if x + n > n * n - 1:
            moves.remove('↓') #Down
        return moves

    def expand(self, n):
        x = self.state.index(0)
        moves = self.available_moves(x, n)
        children = []
        for direction in moves:
            temp = self.state.copy()
            if direction == '←': #Left
                temp[x], temp[x - 1] = temp[x - 1], temp[x]
            elif direction == '→': #Right
                temp[x], temp[x + 1] = temp[x + 1], temp[x]
            elif direction == '↑': #Up
                temp[x], temp[x - n] = temp[x - n], temp[x]
            elif direction == '↓': #Down
                temp[x], temp[x + n] = temp[x + n], temp[x]
            children.append(State(temp, self, direction, self.depth + 1, 1, self.goal))
        return children

    def solution(self):
        solution = []
        solution.append(self.direction)
        path = self
        while path.parent is not None:
            path = path.parent
            solution.append(path.direction)
        solution = solution[:-1]
        solution.reverse()
        return solution

def a_star_search(given_state, n, verbose=False):  # Add a 'verbose' parameter
    # Start measuring the time
    start_time = time()
    frontier = PriorityQueue()
    explored = []
    counter = 0
    goal= determine_goal_state(given_state)
    root = State(given_state, None, None, 0, 0, goal)
    if root.has_letters():
        evaluation = root.manhattan_modified(n)
    else:
        evaluation = root.manhattan_distance(n)
    frontier.put((evaluation, counter, root))

    while not frontier.empty():
        current_node = frontier.get()
        current_node = current_node[2]
        explored.append(current_node.state)

        if current_node.is_goal():
            if verbose:  # Check if verbose is True
                   print_board_solution(given_state,current_node.solution())
            # Calculate the time taken for this run
            end_time = time()
            elapsed_time = end_time - start_time
            print(f"Time taken: {elapsed_time} seconds")
            return current_node.solution(), len(explored)

        children = current_node.expand(n)
        for child in children:
            if child.state not in explored:
                counter += 1
                if child.has_letters():
                    evaluation = child.manhattan_modified(n)
                else:
                    evaluation = child.manhattan_distance(n)
                frontier.put((evaluation, counter, child))
                
    # Calculate the time taken if no solution is found
    end_time = time()
    elapsed_time = end_time - start_time
    print(f"No solution found. Time taken: {elapsed_time} seconds")
    return None

def determine_goal_state(pattern):
    GOAL_STATE_1 = [1, 2, 3, 4, 'a', 'a', 'a', 'a', 0]
    GOAL_STATE_2 = ['a', 'a', 'a', 'a', 5, 6, 7, 8, 0]
    GOAL_STATE_COMPLETE = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    if set(pattern) == set(GOAL_STATE_1):
        return GOAL_STATE_1
    elif set(pattern) == set(GOAL_STATE_2):
        return GOAL_STATE_2
    elif set(pattern) == set(GOAL_STATE_COMPLETE):
        return GOAL_STATE_COMPLETE
    else:
        return "Pattern does not match any goal state"

def print_state(state, n):
    for i in range(n):
        row = state[i * n:(i + 1) * n]
        print(" | ".join(map(str, row)))
        if i < n - 1:
            print("-" * (n * 4 - 1))  # Separator between rows
    print("\n")


def print_board_solution(root, solution, horizontal=False):
    n = int(len(root) ** 0.5)
    current_state = root.copy()

    print("initial:")
    print_state(current_state, n)

    for move in solution:
        if move == '←':  # Left
            x = current_state.index(0)
            current_state[x], current_state[x - 1] = current_state[x - 1], current_state[x]
        elif move == '→':  # Right
            x = current_state.index(0)
            current_state[x], current_state[x + 1] = current_state[x + 1], current_state[x]
        elif move == '↑':  # Up
            x = current_state.index(0)
            current_state[x], current_state[x - n] = current_state[x - n], current_state[x]
        elif move == '↓':  # Down
            x = current_state.index(0)
            current_state[x], current_state[x + n] = current_state[x + n], current_state[x]

        print(move + ":")
        print_state(current_state, n)

def create_patterns(input_list):
    pattern1 = []
    pattern2 = []

    for num in input_list:
        if num == 0:
            pattern1.append(num)
            pattern2.append(num)
        elif 1 <= num <= 4:
            pattern1.append(num)
            pattern2.append('a')
        elif 5 <= num <= 8:
            pattern1.append('a')
            pattern2.append(num)
        else:
            pattern1.append('a')
            pattern2.append('a')

    return pattern1, pattern2

def number_of_moves(input_list):
    n = 3
    result= []
    cost=0
    patterns = create_patterns(input_list)
    for root in patterns:
        print(root)
        result.append(root)
    for root in patterns:
        a_star_solution = a_star_search(root, n, verbose=False)  # Enable verbose output
        number_of_moves = len(a_star_solution[0])
        result.append(number_of_moves)
        #print('Number of movements is ', number_of_moves)
        cost += number_of_moves
    result.append(cost)
    return result

def inv_num(puzzle):
    inv = 0
    for i in range(len(puzzle)-1):
        for j in range(i + 1, len(puzzle)):
            if puzzle[i] > puzzle[j] and puzzle[i] and puzzle[j]:
                inv += 1
    return inv

def solvable(puzzle):
    inv_counter = inv_num(puzzle)
    return inv_counter % 2 == 0
# input_list = [1, 8, 2, 0, 4, 3, 7, 6, 5]
# resultado=number_of_moves(input_list)
# print(resultado)
