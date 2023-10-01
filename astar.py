from queue import PriorityQueue
from time import time
from conection_database import select_heuristic_by_state, create_connection
# Global variable to store memoized heuristic values
memoized_heuristics = {}

#revisited
class State:
    DIRECTIONS = ['←', '→', '↑', '↓']

    def __init__(self, state, parent, direction, depth, cost, goal, n):
        self.state = state
        self.parent = parent
        self.direction = direction
        self.depth = depth
        self.goal = goal
        self.n = n
        self.valid_moves = self.calculate_valid_moves()
        self.state_tuple = tuple(self.state)

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

    def manhattan_distance(self):
        if self.state_tuple in memoized_heuristics:
            return memoized_heuristics[self.state_tuple]

        heuristic = 0
        for i in range(1, self.n * self.n):
            distance = abs(self.state_tuple.index(i) - self.goal.index(i))
            heuristic = heuristic + distance // self.n + distance % self.n

        a_star_evaluation = heuristic + self.cost

        memoized_heuristics[self.state_tuple] = a_star_evaluation  # Memoize the heuristic value
        return a_star_evaluation

    def manhattan_modified(self):
        if self.state_tuple in memoized_heuristics:
            return memoized_heuristics[self.state_tuple]

        heuristic = 0
        for i in range(1, self.n * self.n):
            if i != 'a':
                distance = abs(i - (i - 1) // self.n) + abs((i - 1) % self.n - (i - 1) // self.n)
                heuristic += distance

        AStar_evaluation = heuristic + self.cost
        memoized_heuristics[self.state_tuple] = AStar_evaluation
        return AStar_evaluation
    
    def disjoint_pattern_database(self,conn):
        if self.state_tuple in memoized_heuristics:
            return memoized_heuristics[self.state_tuple]
        heuristic= select_heuristic_by_state(conn, self.state)
        
        AStar_evaluation = heuristic + self.cost
        memoized_heuristics[self.state_tuple] = AStar_evaluation
        return AStar_evaluation
    
    def expand(self):
        x = self.state.index(0)
        moves = self.valid_moves  # Use the precalculated valid moves
        children = []

        for direction in moves:
            temp = self.state[:]  # Create a shallow copy of the current state

            if direction == '←':  # Left
                temp[x], temp[x - 1] = temp[x - 1], temp[x]
            elif direction == '→':  # Right
                temp[x], temp[x + 1] = temp[x + 1], temp[x]
            elif direction == '↑':  # Up
                temp[x], temp[x - self.n] = temp[x - self.n], temp[x]
            elif direction == '↓':  # Down
                temp[x], temp[x + self.n] = temp[x + self.n], temp[x]

            children.append(State(temp, self, direction, self.depth + 1, 1, self.goal, self.n))

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

    def calculate_valid_moves(self):
        x = self.state.index(0)
        valid_moves = State.DIRECTIONS.copy()

        if x % self.n == 0:
            valid_moves.remove('←')  # Left
        if x % self.n == self.n - 1:
            valid_moves.remove('→')  # Right
        if x - self.n < 0:
            valid_moves.remove('↑')  # Up
        if x + self.n > self.n * self.n - 1:
            valid_moves.remove('↓')  # Down

        return valid_moves


def a_star_search(given_state, n, verbose=False, getTime=False,heuristic='m'):
    # Create a connection to the database
    conn=create_connection()
    # Start measuring the time
    start_time = time()
    frontier = PriorityQueue()
    explored = set()  # Use a set to store explored states
    counter = 0
    goal = determine_goal_state(given_state, n)
    root = State(given_state, None, None, 0, 0, goal, n)
    
    # Convert the root state to a tuple for use in explored set
    explored.add(tuple(root.state))
    
    if root.has_letters():
        evaluation = root.manhattan_modified()
    else:
        if heuristic == 'd':
            evaluation = root.disjoint_pattern_database(conn)
        elif heuristic == 'm':
            evaluation = root.manhattan_distance()
    
    frontier.put((evaluation, counter, root))

    while not frontier.empty():
        current_node = frontier.get()
        current_node = current_node[2]
        explored.add(tuple(current_node.state))  # Convert the list to a tuple and add to explored set

        if current_node.is_goal():
            if verbose:
                print_board_solution(given_state, current_node.solution())
            # Calculate the time taken for this run
            end_time = time()
            elapsed_time = end_time - start_time
            if getTime:
                print(f"Time taken: {elapsed_time} seconds")
            return current_node.solution(), len(explored)

        children = current_node.expand()
        for child in children:
            child_tuple = tuple(child.state)
            if child_tuple not in explored:
                counter += 1
                if child.has_letters():
                    evaluation = child.manhattan_modified()
                else:
                    evaluation = child.manhattan_distance()
                frontier.put((evaluation, counter, child))

    # Calculate the time taken if no solution is found
    end_time = time()
    elapsed_time = end_time - start_time
    print(f"No solution found. Time taken: {elapsed_time} seconds")
    return None

def number_of_moves(input_list,n):
    result = [] 
    cost = 0
    patterns = create_patterns(input_list,n)
    for pattern in patterns:
        result.append(pattern)
    for pattern in patterns:
        print('/n solving: ',pattern)
        a_star_solution = a_star_search(pattern, n, verbose=False,heuristic='m')
        number_of_moves = len(a_star_solution[0])
        print('/n cost: ',number_of_moves)
        result.append(number_of_moves)
        cost += number_of_moves
    result.append(cost)
    return result  #########


def create_patterns(input_list,n):
    if n == 3:
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
    if n ==4:
        pattern1 = []
        pattern2 = []
        pattern3 = []
        for num in input_list:
            if num == 0:
                pattern1.append(num)
                pattern2.append(num)
                pattern3.append(num)
            elif num in [2,3,4]:
                pattern1.append('a')
                pattern2.append(num)
                pattern3.append('a')
            elif num in [1, 5, 6, 9, 10, 13]:
                pattern1.append(num)
                pattern2.append('a')
                pattern3.append('a')
            elif num in [7, 8, 11, 12, 14, 15]:
                pattern1.append('a')
                pattern2.append('a')
                pattern3.append(num)
        # print(pattern1,'\n')
        # print(pattern2,'\n')
        # print(pattern3,'\n')
        return pattern1, pattern2, pattern3
    else:
        return None

def determine_goal_state(pattern,n):
    if n ==3:
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
    if n == 4:
        GOAL_STATE_1 = [1, 'a', 'a', 'a', 5, 6, 'a', 'a', 9, 10, 'a', 'a', 13, 'a', 'a', 0] 
        GOAL_STATE_2 = ['a', 2, 3, 4, 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 0] 
        GOAL_STATE_3 = ['a', 'a', 'a', 'a', 'a', 'a', 7, 8, 'a', 'a', 11, 12, 'a', 14, 15, 0] 
        GOAL_STATE_COMPLETE = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]

        if set(pattern) == set(GOAL_STATE_1):
            print("Goal state 1")
            return GOAL_STATE_1
        elif set(pattern) == set(GOAL_STATE_2):
            print("Goal state 2")
            return GOAL_STATE_2
        elif set(pattern) == set(GOAL_STATE_2):
            print("Goal state 3")
            return GOAL_STATE_3
        elif set(pattern) == set(GOAL_STATE_COMPLETE):
            print("Goal state complete")
            return GOAL_STATE_COMPLETE
        else:
            return "Pattern does not match any goal state"




#functional
def print_state(state, n):
    max_width = len(str(n * n - 1))  # Determine the maximum width for elements
    for i in range(n):
        row = state[i * n:(i + 1) * n]
        formatted_row = [f"{item:>{max_width}}" if item != 0 else " " * max_width for item in row]
        print(" | ".join(formatted_row))
        if i < n - 1:
            print("-" * (n * (max_width + 3) - 1))  # Separator between rows
    print("\n")

def print_board_solution(root, solution):
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

def inv_num(puzzle):
    inv = 0
    for i in range(len(puzzle) - 1):
        for j in range(i + 1, len(puzzle)):
            if puzzle[i] > puzzle[j] and puzzle[i] and puzzle[j]:
                inv += 1
    return inv

def solvable(puzzle):
    inv_counter = inv_num(puzzle)
    return inv_counter % 2 == 0


# Example input_list
# input_list = [1, 8, 2, 0, 4, 3, 7, 6, 5]
# result = number_of_moves(input_list,n=3)
# print(result)




# root2 = [1,2,3,4,5,6,7,0,10,13,8,9,14,12,15,11]

# print("\n \n The given state is:", root2)

# if solvable(root2):
#     print("Solvable, please wait.\n")

#     a_star_solution2 = a_star_search(root2, n=4,verbose=False,getTime=True)  # Enable verbose output
#     print('A* Solution is ', a_star_solution2[0])
#     print('Number of explored nodes is ', a_star_solution2[1])
# else:
#     print("Not solvable")




# Not computing: 
# print('\n \n \n  \n')
# input_list2 = [1,2,3,4,5,6,7,0,10,13,8,9,14,12,15,11]
# result = number_of_moves(input_list2,n=4)
# print(result)




# #optimization testing:
# import cProfile

# def main_function_name():
#     # Call the function you want to profile here
#     # input_list = [1, 8, 2, 0, 4, 3, 7, 6, 5]
#     # result = number_of_moves(input_list, n=3)
#     # print(result)

#     # root2 = [1,2,3,4,5,6,7,0,10,13,8,9,14,12,15,11]
#     # print("\n \n The given state is:", root2)

#     # if solvable(root2):
#     #     print("Solvable, please wait.\n")

#     #     a_star_solution2 = a_star_search(root2, n=4,verbose=False,getTime=True)  # Enable verbose output
#     #     print('A* Solution is ', a_star_solution2[0])
#     #     print('Number of explored nodes is ', a_star_solution2[1])
#     # else:
#     #     print("Not solvable")


#     # input_list2 = [1,2,3,4,5,6,7,0,10,13,8,9,14,12,15,11]
#     # result = number_of_moves(input_list2,n=4)
#     # print(result)

    
#     a_star_solution2 = a_star_search(['a', 2, 3, 'a', 'a',4, 'a', 0, 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'], n=4,verbose=False,getTime=True)  # Enable verbose output
#     print('A* Solution is ', a_star_solution2[0])
#     print('Number of explored nodes is ', a_star_solution2[1])

    
#     # a_star_solution2 = a_star_search(['a', 'a', 'a', 'a', 'a', 'a', 7, 0, 'a', 'a', 8, 'a', 14, 12, 15, 11], n=4,verbose=False,getTime=True)  # Enable verbose output
#     # print('A* Solution is ', a_star_solution2[0])
#     # print('Number of explored nodes is ', a_star_solution2[1])

# if __name__ == "__main__":
#     cProfile.run("main_function_name()", sort="cumulative")



