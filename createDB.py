import json
import os
import time  # Import the time module
from astar import number_of_moves 
# Function to process a batch of entries (1000 at a time)
def process_batch(puzzles, start_index, batch_size):
    end_index = start_index + batch_size
    if end_index > len(puzzles):
        end_index = len(puzzles)

    for index in range(start_index, end_index):
        # Process the puzzle here (you can replace this with your actual processing logic)
        puzzle = puzzles[index]
        puzzle["visited"] = True
        response = number_of_moves(puzzle["state"])
        # print(puzzle["state"])
        puzzle["state_1"] = response[0]
        puzzle["state_2"] = response[1]
        puzzle["cost_1"] = response[2]
        puzzle["cost_2"] = response[3]
        puzzle["cost_total"] = response[4]
    return puzzles

# Function to save the current state to a JSON file in the /batches folder
def save_progress_to_json(puzzles, batch_number):
    folder_path = "batches"
    os.makedirs(folder_path, exist_ok=True)
    progress_filename = os.path.join(folder_path, f"progress_batch_{batch_number}.json")
    with open(progress_filename, 'w') as json_file:
        json.dump(puzzles, json_file, indent=4)

# Function to save the configuration data (last_completed_batch and current_index) to a JSON file
def save_configuration(config_data):
    with open("config.json", 'w') as config_file:
        json.dump(config_data, config_file, indent=4)

# Function to load the configuration data (last_completed_batch and current_index) from a JSON file
def load_configuration():
    if os.path.exists("config.json"):
        with open("config.json", 'r') as config_file:
            return json.load(config_file)
    else:
        return {"last_completed_batch": 0, "current_index": 0}

def CreateDatabase(batch_size=5000):
    print("Starting the script...")

    # Create the /batches folder if it doesn't exist
    os.makedirs("batches", exist_ok=True)

    # Check if there are batch files in the /batches folder
    batch_files = [filename for filename in os.listdir("batches") if filename.startswith("progress_batch_")]

    if batch_files:
        # If there is more than one batch, start from the batch before the last one
        if len(batch_files) > 1:
            last_batch = sorted(batch_files)[-1]
            last_batch_number = int(last_batch.split("_")[-1].split(".")[0])
            second_last_batch_number = last_batch_number - 1
            json_filename = os.path.join("batches", f"progress_batch_{second_last_batch_number}.json")
            print(f"Resuming from batch {second_last_batch_number}...")
        else:
            # If there is only one batch, start from the initial JSON file
            json_filename = "solvable_puzzles.json"
            print("No previous batches found, starting from the initial JSON file...")

            # Set configuration data to zeros
            config_data = {"last_completed_batch": 0, "current_index": 0}
            save_configuration(config_data)
    else:
        # If no batch files exist, start from the initial JSON file
        json_filename = "solvable_puzzles.json"
        print("No previous batches found, starting from the initial JSON file...")

        # Set configuration data to zeros
        config_data = {"last_completed_batch": 0, "current_index": 0}
        save_configuration(config_data)

    # Load the JSON file to begin processing
    if os.path.exists(json_filename):
        with open(json_filename, 'r') as json_file:
            puzzles = json.load(json_file)
    else:
        print("JSON file not found.")
        return

    # Load the configuration data (last_completed_batch and current_index)
    config_data = load_configuration()
    last_completed_batch = config_data["last_completed_batch"]
    current_index = config_data["current_index"]

    while current_index < len(puzzles):
        # Start measuring the time for this batch
        batch_start_time = time.time()

        # Process the current batch
        puzzles = process_batch(puzzles, current_index, batch_size)
        current_index += batch_size

        # Save the progress to a new JSON file in the /batches folder
        save_progress_to_json(puzzles, last_completed_batch)

        # Calculate the time taken for this batch
        batch_end_time = time.time()
        batch_elapsed_time = batch_end_time - batch_start_time

        print(f"Processed batch {last_completed_batch} - Entries processed: {current_index}/{len(puzzles)}")
        print(f"Time taken for this batch: {batch_elapsed_time} seconds")

        # Update the last_completed_batch and current_index in the configuration data
        last_completed_batch += 1
        config_data["last_completed_batch"] = last_completed_batch
        config_data["current_index"] = current_index

        # Save the updated configuration data
        save_configuration(config_data)

    print("Processing complete. All batches have been processed and saved in the /batches folder.")
    print("Script finished.")

if __name__ == "__main__":
    CreateDatabase(batch_size=18000)
