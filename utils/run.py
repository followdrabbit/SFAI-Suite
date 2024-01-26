import openai
from dotenv import load_dotenv
import os

def run_thread(thread_id, assistant_id):
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
        run = openai.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
        print(f"Thread run was created with ID: {run.id}")
        return (run.id)

    except Exception as e:
        print(f"Error running the thread: {e}")
