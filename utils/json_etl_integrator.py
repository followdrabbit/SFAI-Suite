# Import necessary libraries
import json  # Used for working with JSON data
import asyncio  # Used for writing concurrent code using async/await syntax
import os

# Defines a class named JsonETLIntegrator
class JsonETLIntegrator:
    def __init__(self):
        pass  # This is the constructor of the class. It currently does nothing.

    # Asynchronous method to read a JSON file
    async def read_json_file(self, file_path):
        # Verifies if the file path exists and is a file
        if not os.path.exists(file_path):
            print("Error: File path does not exist.")
            return None
        if not os.path.isfile(file_path):
            print("Error: The path is not a file.")
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as file:  # Opens the file at the provided path
                return json.load(file)  # Loads and returns the JSON data from the file
        except Exception as e:
            # Handles any exception that might occur during file opening or JSON loading
            print(f"An error occurred while reading the file: {e}")
            return None

    # Asynchronous method to extract information from a list of messages
    async def extract_raw_info(self, messages):
        for message in messages:  # Iterates over each message in the list
            if message['role'] == 'assistant':  # Checks if the role of the message is 'assistant'
                message_content = message['message'].strip()  # Removes any leading/trailing whitespace
                if not message_content:
                    print("The message is empty or not valid.")
                    return None
                try:
                    # Tries to decode the message content as JSON
                    json_data = json.loads(message_content)
                    return json_data  # Returns the Python object obtained from JSON
                except json.JSONDecodeError as e:
                    # Catches and prints any JSON decoding error
                    print("Error decoding JSON:", e)
                    print("JSON content:", message_content)  # Prints the content for debugging
                    return None

        return None  # Returns None if no valid message is found



# Defines an asynchronous main function
async def main():
    integrator = JsonETLIntegrator()  # Creates an instance of JsonETLIntegrator class
    # Reads a JSON file and stores the data
    #json_data = await integrator.read_json_file('path/to/data.json')
    # json_data = await integrator.read_json_file('../data/raw/0001_controls_20240128_191542_raw.json')
    # print(json_data)  # Prints the JSON data

    # Defines a list of example messages
    # messages = [
    #     {"role": "user", "message": "Hello, this is a test."},
    #     {"role": "assistant", "message": "```json\n{\"key\": \"value\"}\n```"}
    # ]

    # Extracts JSON data from the messages
    # extracted_json = await integrator.extract_raw_info(json_data)
    # print(extracted_json)  # Prints the extracted JSON data

# Runs the main function
asyncio.run(main())
