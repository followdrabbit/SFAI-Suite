import openai
from dotenv import load_dotenv
import os
from utils.text_replacer import replace_text_in_file

def create_thread(prompt_path, variable_to_replace, technology):
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
        # Create a new thread to communicate with the assistant
        thread = openai.beta.threads.create()

        # Send a message to the assistant within the thread using the loaded request content
        message = openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=replace_text_in_file(prompt_path, variable_to_replace, technology)
        )

        # Inform that the thread has been successfully created and show its ID
        print(f"Thread created successfully with ID: {thread.id}")

        # Save the raw response to a file, naming it based on the thread ID
        file_path = os.path.join('data', f'{thread.id}_thread.txt')
        with open(file_path, 'w') as outfile:
            outfile.write(str(message))  # Save the raw string representation
        
        # Return th Id for the thread
        return (thread.id)

    except Exception as e:
        print(f"Error communicating with the assistant: {e}")
