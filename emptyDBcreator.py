import json
from astar import solvable
from itertools import permutations

def generate_and_check_puzzles():
    n = 3
    goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    all_puzzles = list(permutations(goal_state))
    solvable_puzzles = []

    for puzzle in all_puzzles:
        puzzle = list(puzzle)
        if solvable(puzzle):
            solvable_puzzles.append({
                "state": puzzle,
                "visited": False,
                "state_1": None,
                "state_2": None,
                "cost_1": None,
                "cost_2": None,
                "cost_total": None
            })

    print("\nTotal solvable puzzles:", len(solvable_puzzles))
    return solvable_puzzles

def save_puzzles_to_json(puzzles, filename):
    with open(filename, 'w') as json_file:
        json.dump(puzzles, json_file, indent=4)

def retrieve_state_info(json_filename, target_state):
    with open(json_filename, 'r') as json_file:
        puzzles = json.load(json_file)

    for puzzle in puzzles:
        if puzzle["state"] == target_state:
            return puzzle

    return None
    
if __name__ == "__main__":
    solvable_puzzles = generate_and_check_puzzles()

    # Save solvable puzzles to a JSON file
    json_filename = "solvable_puzzles.json"
    save_puzzles_to_json(solvable_puzzles, json_filename)
    print("Solvable puzzles saved to", json_filename)

    target_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    retrieved_info = retrieve_state_info(json_filename, [1, 8, 2, 0, 4, 3, 7, 6, 5])

    if retrieved_info:
        print("\nInformation for target state:")
        print("State:", retrieved_info["state"])
        print("Visited:", retrieved_info["visited"])
        print("State_1:", retrieved_info["state_1"])
        print("State_2:", retrieved_info["state_2"])
        print("Cost_1:", retrieved_info["cost_1"])
        print("Cost_2:", retrieved_info["cost_2"])
        print("Cost_total:", retrieved_info["cost_total"])
    else:
        print("\nState is not solvable")

    retrieved_info2 = retrieve_state_info(json_filename, [2,1,3,4,5,6,7,8,0])

    if retrieved_info2:
        print("\nInformation for target state:")
        print("State:", retrieved_info2["state"])
        print("Visited:", retrieved_info2["visited"])
        print("State_1:", retrieved_info2["state_1"])
        print("State_2:", retrieved_info2["state_2"])
        print("Cost_1:", retrieved_info2["cost_1"])
        print("Cost_2:", retrieved_info2["cost_2"])
        print("Cost_total:", retrieved_info2["cost_total"])
    else:
        print("\nState is not solvable")