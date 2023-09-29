from astar import solvable
from astar import a_star_search

# User interface
n = 3
root = [1, 8, 2, 0, 4, 3, 7, 6, 5]

print("The given state is:", root)


if solvable(root):
    print("Solvable, please wait.\n")

    a_star_solution = a_star_search(root, n, verbose=True)  # Enable verbose output
    print('A* Solution is ', a_star_solution[0])
    print('Number of explored nodes is ', a_star_solution[1])


else:
    print("Not solvable")