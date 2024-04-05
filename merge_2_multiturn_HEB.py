import json
import os

def merge_json_files(input_dir, output_file):
    # Initialize merged data
    merged_data = {"id": 1, "length": 0, "conversations": []}

    # Get a list of all JSON files in the input directory
    json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]

    # Read each file and collect data
    current_id = 1
    all_conversations = []  # A single array to hold all conversations
    for json_file in sorted(json_files):  # Sort files based on their names
        with open(os.path.join(input_dir, json_file), 'r', encoding='utf-8') as f:
            data = json.load(f)

            # Ensure data is a list
            if isinstance(data, list):
                conversations = data
            else:
                conversations = data.get("conversations", [])

            # Append each conversation to the merged data
            for conversation in sorted(conversations, key=lambda x: x.get("id", 0)):  # Sort conversations based on their id
                conversation["id"] = current_id

                # Calculate the combined length of characters in "human" and "gpt" values
                combined_length = sum(len(conv["value"]) for conv in conversation["conversations"] if conv.get("from") in ["gpt", "human"])
                conversation["length"] = combined_length

                all_conversations.extend(conversation["conversations"])  # Append the entire conversation

                current_id += 1

    # Update merged data with all conversations and total length
    merged_data["conversations"] = all_conversations
    merged_data["length"] = sum(len(conv["value"]) for conv in all_conversations)

    # Write the merged data to the output file
    with open(output_file, 'w', encoding='utf-8') as out_file:
        json.dump([merged_data], out_file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    input_directory = "."  # Change this to your input directory
    output_file = "merged_output.json"  # Change this to your desired output file

    merge_json_files(input_directory, output_file)
