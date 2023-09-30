from astar import solvable
from astar import a_star_search

# User interface

root = [1, 8, 2, 0, 4, 3, 7, 6, 5]

print("The given state is:", root)

if solvable(root):
    print("Solvable, please wait.\n")

    a_star_solution = a_star_search(root, n=3, verbose=False, getTime=True)  # Enable verbose output
    print('A* Solution is ', a_star_solution[0])
    print('Number of explored nodes is ', a_star_solution[1])
else:
    print("Not solvable")


root2 = [1,2,3,4,5,6,7,0,10,13,8,9,14,12,15,11]

print("\n \n The given state is:", root2)

if solvable(root2):
    print("Solvable, please wait.\n")

    a_star_solution2 = a_star_search(root2, n=4,verbose=False,getTime=True)  # Enable verbose output
    print('A* Solution is ', a_star_solution2[0])
    print('Number of explored nodes is ', a_star_solution2[1])
else:
    print("Not solvable")