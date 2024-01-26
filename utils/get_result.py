import time
import openai
from dotenv import load_dotenv
import os


def check_assistant_status(thread_id, run_id, assistant_id):

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
        print("Checking assistant status.")
        while True:
            run = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

            if run.status == "completed":
                print("Done!")
                messages = openai.beta.threads.messages.list(thread_id=thread_id)

                result_messages = []
                print("Messages:")
                for message in messages:
                    assert message.content[0].type == "text"
                    msg = {"role": message.role, "message": message.content[0].text.value}
                    print(msg)
                    result_messages.append(msg)

                openai.beta.assistants.delete(assistant_id)

                return result_messages
            else:
                print("In progress...")
                time.sleep(5)

    except Exception as e:
        print(f"Error checking the assistant status: {e}")