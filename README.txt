astar.py provides an extensible implementation of the A* search algorithm for solving sliding puzzles, including the option to use different heuristics and pattern databases for more efficient solving.

populateDBmultiThread.py is a python script that uses multithreading to process a list of states stored in the SQLite database. Where the main function connects to an SQLite database named 'puzzle_database_3x3.db', and selects all entries where the 'visited' column is 0 and 'cost_total' column is NULL. It iterates through the unvisited states and submits them to a thread pool for processing concurrently and measures the elapsed time and prints statistics.

populateDB.py is a script for processing states in a puzzle database using a custom function number_of_moves. The script first checks if the database file for the given n exists and provides a message if it doesn't exist, suggesting to run a script to create it. It connects to the SQLite database and selects all entries where 'visited' is 0 and 'cost_total' is NULL. It iterates through the unvisited states and processes them one by one using the number_of_moves function. After processing a certain number of states (defined by x), it prints the elapsed time, and finally, it prints the total number of visited states and the total time taken to visit all states.

createSolvableDB3X3.py defines two functions and then calls them to create a SQLite database and generate/check permutations of a 3x3 puzzle. If a permutation is solvable, it inserts the puzzle into the database with appropriate information and increments the solvable_count. After processing all permutations, it commits the changes to the database, closes the connection, and prints the total count of solvable puzzles.

conection_database.py provides a way to connect to the SQLite database and retrieve the cost associated with a specific puzzle state by querying the database

client.py take user input for a 3x3 puzzle state and then determine if the puzzle is solvable using the solvable() function. If the puzzle is solvable, it runs two different A* search algorithms to find solutions, one using the Manhattan heuristic and the other using the Disjoint pattern database heuristic.

Modo de Uso 

Por el momento solo se soporta completamente puzzles de 3x3, implementacion 4x4 en progreso. (Cuello de botella, generar base de datos para 4x4)

Creación de la base de datos:
    Utilizar createSolvableDBnxn.py para generar una base de datos vacia, que contienene todas las combinaciones con solucion.
    Utilizar populateDB (multiThread preferiblemente) para llenar la base de datos con las soluciones de la heuristica.
    Se generará el archivo puzzle_database_nxn.db, el programa utilza actualmente el archivo nxnDataBase.db para la resolución de problemas.

