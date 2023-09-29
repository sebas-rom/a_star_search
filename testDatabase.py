import sqlite3

def retrieve(state):
    conn = sqlite3.connect('puzzle_database.db')
    cursor = conn.cursor()

    # Retrieve data for the given state
    cursor.execute('SELECT * FROM puzzles WHERE state = ?', (state,))
    result = cursor.fetchone()

    if result:
        state, visited, sub_state_1, sub_state_2, cost_1, cost_2, cost_total = result
        print("State:", state)
        print("Visited:", visited)
        print("sub_State_1:", sub_state_1)
        print("sub_State_2:", sub_state_2)
        print("Cost_1:", cost_1)
        print("Cost_2:", cost_2)
        print("Cost_total:", cost_total)
    else:
        print("unsolvable:  not found in the database")

    conn.close()

def write(key, value, state):
    conn = sqlite3.connect('puzzle_database.db')
    cursor = conn.cursor()

    # Check if the state exists in the database
    cursor.execute('SELECT state FROM puzzles WHERE state = ?', (state,))
    existing_state = cursor.fetchone()

    if existing_state:
        # Update the specified key with the new value
        cursor.execute(f'UPDATE puzzles SET {key} = ? WHERE state = ?', (value, state))
        conn.commit()
        print(f"Updated {key} for state {state}")
    else:
        print("unsolvable: State not found in the database")

    conn.close()


write('visited', 1, "2,1,3,4,5,6,7,8,0")
retrieve('2,1,3,4,5,6,7,8,0')

write('sub_state_1', '1,2,3,4,a,a,a,a,0', "1,2,3,4,5,6,7,8,0")
write('sub_state_2', 'a,a,a,a,5,6,7,8,0', "1,2,3,4,5,6,7,8,0")
retrieve('1,2,3,4,5,6,7,8,0')