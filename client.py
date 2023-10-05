from astar import solvable
from astar import a_star_search
from conection_database import create_connection
# User interface

n = 3
print("Enter your" ,n,"*",n, "puzzle")
# root = [1,8,2,0,4,3,7,6,5]
root = [0,8,7,6,5,4,3,2,1]
#
# num= input()
# for x in str(num):
#   root.append(int(x))
  
print("The given state is:", root)

if solvable(root):
    print("Solvable, please wait.\n")

    a_star_solution_manhattan = a_star_search(root, n=3, verbose=True, getTime=True,heuristic='m',mem_heuristics=False)  
    print('A* Solution is with Manhattan is ', a_star_solution_manhattan[0])
    print('Number of explored nodes is ', a_star_solution_manhattan[1])
    # print('Number of frontier nodes is ', a_star_solution_manhattan[2], '\n')   
    
    a_star_solution_disjoint = a_star_search(root, n=3, verbose=False, getTime=True,heuristic='d',mem_heuristics=False)  # Enable verbose output
    print('A* Solution is with Disjoint is ', a_star_solution_disjoint[0])
    print('Number of explored nodes is ', a_star_solution_disjoint[1])
    # print('Number of frontier nodes is ', a_star_solution_disjoint[2], '\n')
else:
    print("Not solvable")

#123460875
# root2 = [1,2,3,4,5,6,7,0,10,13,8,9,14,12,15,11]

# print("\n \n The given state is:", root2)

# if solvable(root2):
#     print("Solvable, please wait.\n")

#     a_star_solution2 = a_star_search(root2, n=4,verbose=False,getTime=True)  # Enable verbose output
#     print('A* Solution is ', a_star_solution2[0])
#     print('Number of explored nodes is ', a_star_solution2[1])
# else:
#     print("Not solvable")