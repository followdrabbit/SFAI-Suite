import openai
import asyncio
import time
import os
from dotenv import load_dotenv

class OpenAIRunsManager:
    def __init__(self, api_key):
        self.client = openai.AsyncClient(api_key=api_key)

    async def create_run(self, thread_id: str, assistant_id: str):
        run = await self.client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)
        print(f"New run created with ID: {run.id}")
        return run.id

    async def retrieve_run(self, thread_id: str, run_id: str):
        return await self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

    async def list_run(self, thread_id: str):
        return await self.client.beta.threads.runs.list(thread_id=thread_id)

    async def cancel_run(self, thread_id: str, run_id: str):
        return await self.client.beta.threads.runs.cancel(thread_id=thread_id, run_id=run_id)

    async def process_run(self, thread_id: str, run_id: str, ticket: str):
        try:
            print("Checking run status.")
            while True:
                run = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

                if run.status == "completed":
                    print("Run Completed")
                    messages = openai.beta.threads.messages.list(thread_id=thread_id)

                    result_messages = []
                    # print("Messages:")
                    for message in messages:
                        assert message.content[0].type == "text"
                        msg = {"role": message.role, "message": message.content[0].text.value}
                        #print(msg)
                        result_messages.append(msg)
                    return result_messages
                else:
                    print("In progress...")
                    time.sleep(5)

        except Exception as e:
            print(f"Error checking the run status: {e}")


async def main():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    run_manager = OpenAIRunsManager(api_key)

    # Substitua 'your_thread_id' e 'your_assistant_id' pelos valores apropriados
    #run_id = await run_manager.create_run('your_thread_id', 'your_assistant_id')
    #print(f"Run ID: {run_id}")

if __name__ == "__main__":
    asyncio.run(main())
