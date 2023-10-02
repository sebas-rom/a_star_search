import sqlite3
from astar import solvable
from itertools import permutations
import os

def create_database():
    # Check if the database file exists and delete it if it does
    if os.path.exists('puzzle_database_4x4.db'):
        os.remove('puzzle_database_4x4.db')

    conn = sqlite3.connect('puzzle_database_4x4.db')
    cursor = conn.cursor()

    # Create a table to store puzzle objects
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS puzzles (
            state TEXT PRIMARY KEY,
            visited BOOLEAN,
            sub_state_1 TEXT,
            sub_state_2 TEXT,
            sub_state_3 TEXT,
            cost_1 INTEGER,
            cost_2 INTEGER,
            cost_3 INTEGER,
            cost_total INTEGER
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database created.")
    

def generate_and_check_puzzles():
    print("Generating puzzles...")
    goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]

    conn = sqlite3.connect('puzzle_database_4x4.db')
    cursor = conn.cursor()
    print("Connected to database...")

    all_puzzles = list(permutations(goal_state))
    solvable_count = 0  # Initialize a count for solvable puzzles
        
    print("Permutations generated...") 

    # for puzzle in all_puzzles:
    #     puzzle = list(puzzle)
    #     puzzle_state = ','.join(map(str, puzzle))  # Convert the state to a comma-separated string

    #    if solvable(puzzle):
    #         # Insert the puzzle object into the database
    #         cursor.execute('''
    #             INSERT OR IGNORE INTO puzzles (state, visited, sub_state_1, sub_state_2, sub_state_3, cost_1, cost_2, cost_3, cost_total)
    #             VALUES (?, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL)
    #         ''', (puzzle_state,))
    #        print(puzzle)
    #        solvable_count += 1  # Increment the count for solvable puzzles

    # conn.commit()
    # conn.close()

    #print("\nTotal solvable puzzles:", solvable_count)  # Print the count of solvable puzzles

create_database()
generate_and_check_puzzles()