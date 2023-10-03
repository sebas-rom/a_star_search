#!/usr/bin/python

import sqlite3
from sqlite3 import Error
def create_connection():
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    db_file='3x3Database.db'
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    
    except Error as e:
        print("Error in opening database:\n")
        print(str(e))
    return conn


def select_heuristic_by_state(conn, state):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    text_state = ','.join(map(str, state))
    cur = conn.cursor()
    cur.execute("SELECT cost_total FROM puzzles WHERE state=?", (text_state,))
    rows = cur.fetchall()
    cost=rows[0][0]
    return cost
        
# def main():
#     state = [1, 8, 2, 0, 4, 3, 7, 6, 5]
    
#     # create a database connection
#     conn = create_connection()
#     with conn:
#         print("1. Query heuristic by state:")
#         print(select_heuristic_by_state(conn, state))

      

# if __name__ == '__main__':
#     main()      