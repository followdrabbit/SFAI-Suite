# Import necessary libraries
import openai
import asyncio
import os
from dotenv import load_dotenv  # Used for loading environment variables

# Define a class to manage interactions with OpenAI's API
class OpenAIRunsManager:
    def __init__(self, api_key):
        # Initialize the manager with an OpenAI API key
        self.client = openai.AsyncClient(api_key=api_key)

    # Asynchronously create a new run
    async def create_run(self, thread_id: str, assistant_id: str):
        run = await self.client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)
        print(f"New run created with ID: {run.id}")
        return run.id

    # Asynchronously retrieve information about a specific run
    async def retrieve_run(self, thread_id: str, run_id: str):
        return await self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

    # Asynchronously list all runs associated with a thread
    async def list_run(self, thread_id: str):
        return await self.client.beta.threads.runs.list(thread_id=thread_id)

    # Asynchronously cancel a specific run
    async def cancel_run(self, thread_id: str, run_id: str):
        return await self.client.beta.threads.runs.cancel(thread_id=thread_id, run_id=run_id)

    # Asynchronously process a run and check its status
    async def process_run(self, thread_id: str, run_id: str):
        try:
            print("Checking run status.")
            while True:
                run = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

                if run.status == "completed":
                    print(f"Run Completed")
                    messages = openai.beta.threads.messages.list(thread_id=thread_id)

                    result_messages = []
                    for message in messages:
                        assert message.content[0].type == "text"
                        msg = {"role": message.role, "message": message.content[0].text.value}
                        result_messages.append(msg)
                    return result_messages
                else:
                    print(f"In progress...")
                    await asyncio.sleep(5)  # Wait for 5 seconds before checking the status again

        except Exception as e:
            print(f"Error checking the run status: {e}")

# Main async function to execute the manager
async def main():
    load_dotenv()  # Load environment variables (like API keys)
    api_key = os.getenv("OPENAI_API_KEY")  # Get the OpenAI API key from environment variables
    run_manager = OpenAIRunsManager(api_key)  # Create an instance of the manager

    # Example usage (commented out)
    # run_id = await run_manager.create_run('your_thread_id', 'your_assistant_id')
    # result_messages = await run_manager.process_run('your_thread_id', run_id, 'your_ticket')
    # print(result_messages)

    # Suponha que você já tenha um thread_id e run_id válidos
    #thread_id = "seu_thread_id"
    #run_id = "seu_run_id"
    
    # Utilizando a função retrieve_run
    #run_info = await run_manager.retrieve_run(thread_id, run_id)
    #print(run_info)

# Entry point of the script
if __name__ == "__main__":
    asyncio.run(main())  # Execute the main function asynchronously
