import os
import json
from datetime import datetime

# Assuming DATA_DIR is predefined somewhere in your environment. If not, define it here.
DATA_DIR = 'data'  # Update this path as per your directory structure

def message_display(message):
    total_width = 60
    fill_char = '#'
    centered_message = message.center(total_width, fill_char)
    print("\n{}\n".format(centered_message))

def extract_response(raw_data):
    """Extracts assistant messages from the raw response."""
    messages = []
    for item in (item for sublist in raw_data for item in (sublist if isinstance(sublist, list) else [sublist])):
        if item.get('role') == 'assistant':
            messages.append(item.get('message', ''))
    extracted_data = " ".join(messages)
    return extracted_data

def save_data(data, technology, base_dir=DATA_DIR):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')  # Ensure timestamp is defined
    try:
        file_path = os.path.join(base_dir, f"{timestamp}_{technology}.json")
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {file_path}")
    except Exception as e:
        print(e)

def replace_text_in_file(file_path, variable_to_replace, new_value):
    """
    Reads the content of a file, replaces all occurrences of a specified variable
    with a new value, and returns the modified content.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()

        modified_content = content.replace(variable_to_replace, new_value)
        return modified_content
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
        return None
    except IOError:
        print(f"Error accessing the file {file_path}.")
        return None

if __name__ == "__main__":
    # Example usage when the script is run directly
    file_path = '../prompts/controls_prompt_en.txt'  # Path to the input file
    variable_to_replace = 'PRODUCT_NAME'  # The variable to be replaced
    new_value = 'SuperSecure'  # The new value for the variable

    # Call the function with the example parameters
    modified_content = replace_text_in_file(file_path, variable_to_replace, new_value)

    if modified_content is not None:
        print(modified_content)
