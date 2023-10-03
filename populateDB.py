import sqlite3
import time
from astar import number_of_moves
import os

def text_state_to_list(text_state):
    try:
        state_list = [int(x) for x in text_state.split(',')]
        return state_list
    except ValueError:
        print("Invalid text state format. Please provide a comma-separated list of integers.")
        return None

def list_to_text_state(state_list):
    try:
        text_state = ','.join(map(str, state_list))
        return text_state
    except Exception as e:
        print("Error converting list to text state:", str(e))
        return None

def visit_unvisited_states(x=100,n=3):
    db_name = ''
    if n == 3:
        db_name = 'puzzle_database_3x3.db'
    elif n == 4:
        db_name = 'puzzle_database_4x4.db'
    else:
        print("Invalid n-size. Please enter 3 or 4.")
        return None

    if not os.path.exists(db_name):
        print(f"The database was not created yet. Run createSolvableDB{n}x{n}.py first.")
        return
    conn = sqlite3.connect(db_name,check_same_thread=True)
    cursor = conn.cursor()

    # Select all entries where visited is 0 and cost_total is null
    cursor.execute('SELECT state FROM puzzles WHERE visited = 0 AND cost_total IS NULL')
    unvisited_states = cursor.fetchall()

    start_time = time.time()  # Record the start time
    count = 0

    for state_tuple in unvisited_states:
        count += 1
        state = state_tuple[0]
        state_list = text_state_to_list(state)
        
        # Call the number_of_moves function to get the updates
        response = number_of_moves(state_list,n)
        
        sub_state_1 = list_to_text_state(response[0])
        sub_state_2 = list_to_text_state(response[1])
        cost_1 = response[2]
        cost_2 = response[3]
        cost_total = response[4]
        
        # Update the visited state to 1
        cursor.execute('UPDATE puzzles SET visited = 1 WHERE state = ?', (state,))
        
        # Populate new values
        cursor.execute('UPDATE puzzles SET sub_state_1 = ? WHERE state = ?', (sub_state_1, state))
        cursor.execute('UPDATE puzzles SET sub_state_2 = ? WHERE state = ?', (sub_state_2, state))
        cursor.execute('UPDATE puzzles SET cost_1 = ? WHERE state = ?', (cost_1, state))
        cursor.execute('UPDATE puzzles SET cost_2 = ? WHERE state = ?', (cost_2, state))
        cursor.execute('UPDATE puzzles SET cost_total = ? WHERE state = ?', (cost_total, state))

        if count % x == 0:
            # Print the elapsed time after every 'x' states have been visited
            end_time = time.time()
            elapsed_time = end_time - start_time
            print("Visited {} states in {:.2f} seconds.".format(count, elapsed_time))

        conn.commit()

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate the final elapsed time

    conn.close()
    print("Visited {} states.".format(count))
    print("Visited the whole database in {:.2f} seconds.".format(elapsed_time))

# Call the function to visit unvisited states and measure the time
if __name__ == "__main__":
    n_size = int(input("Enter the n-size of the board: "))
    visit_unvisited_states(n=n_size)