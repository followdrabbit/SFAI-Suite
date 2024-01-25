import openai
from dotenv import load_dotenv
import os
import json
import datetime

def create_assistant():
    # Load environment variables from the .env file
    load_dotenv()

    # Get the API Key from the environment
    api_key = os.getenv('OPENAI_API_KEY')

    if api_key is None:
        print("Error: OPENAI_API_KEY not found. Please check your .env file.")
        return

    # Set the OpenAI API key
    openai.api_key = api_key

    try:
        # Create a new assistant
        assistant = openai.beta.assistants.create(
            name="Cloud Security Expert",
            instructions="An assistant specialized in cloud information security. Provides expert advice on securing cloud environments, best practices, and compliance standards.",
            tools=[{"type": "code_interpreter"}],
            model="gpt-4",
            # Add or adjust parameters as needed
        )
        print(f"Assistant created successfully: {assistant.id}")

        # Save the assistant information to a JSON file
        save_assistant_info(assistant)
    except Exception as e:
        print(f"Error creating assistant: {e}")

def save_assistant_info(assistant):
    # Define the file path where the information will be saved
    file_path = '../data/assistant_info.json'

    # Get the current date and time
    creation_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Prepare the data for saving
    assistant_data = {
        "id": assistant.id,
        "name": assistant.name,
        "instructions": assistant.instructions,
        "creation_date": creation_date,  # Include the creation date and time
        # Include other fields as needed
    }

    # Write the data to the JSON file
    with open(file_path, 'w') as file:
        json.dump(assistant_data, file, indent=4)

    print(f"Assistant information saved in {file_path}")

if __name__ == "__main__":
    create_assistant()
