import sqlite3
import time
from astar import number_of_moves
from concurrent.futures import ThreadPoolExecutor
import os
import multiprocessing  # Import the multiprocessing module

# Global variable to signal the threads to stop
stop_threads = False

def get_available_threads():
    # Get the number of CPU cores
    num_cores = os.cpu_count()

    # Get the number of available threads
    num_threads = multiprocessing.cpu_count()

    return num_threads

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

def process_state(state_tuple):
    conn = sqlite3.connect('puzzle_database.db', check_same_thread=False)
    cursor = conn.cursor()

    state = state_tuple[0]
    state_list = text_state_to_list(state)

    response = number_of_moves(state_list)

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

    conn.commit()
    conn.close()

    return state

def visit_unvisited_states(x=500, num_threads=get_available_threads()):
    global stop_threads
    print("Using {} threads.".format(num_threads))
    conn = sqlite3.connect('puzzle_database.db', check_same_thread=False)
    cursor = conn.cursor()

    # Select all entries where visited is 0 and cost_total is null
    cursor.execute('SELECT state FROM puzzles WHERE visited = 0 AND cost_total IS NULL')
    unvisited_states = cursor.fetchall()

    start_time = time.time()  # Record the start time
    count = 0

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for state_tuple in unvisited_states:
            if stop_threads:
                break  # Exit the loop if the stop flag is set

            executor.submit(process_state, state_tuple)
            count += 1


    # Wait for all threads to finish before closing the connection
    executor.shutdown()

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate the final elapsed time

    conn.commit()
    conn.close()

    print("Visited {} states.".format(count))
    print("Visited the whole database in {:.2f} seconds.".format(elapsed_time))

# Call the function to visit unvisited states and measure the time
try:
    visit_unvisited_states()
except KeyboardInterrupt:
    stop_threads = True
    print("Program terminated by user.")