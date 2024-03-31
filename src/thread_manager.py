import openai
import asyncio  # This module allows for asynchronous programming.
import os  # This module is used to interact with the operating system.
from typing import Optional  # This is used for optional type hints in function arguments.
from dotenv import load_dotenv  # This module loads environment variables from a .env file.
import tiktoken  # Importing the tiktoken module for tokenization.

# Defining a class to manage OpenAI threads
class OpenAIThreadManager:
    # Constructor for the class, initializes the OpenAI client with an API key
    def __init__(self, api_key):
        self.client = openai.AsyncClient(api_key=api_key)  # Setting up the asynchronous OpenAI client.
        self.encoder = tiktoken.encoding_for_model("gpt-4")  # Setting up the tokenizer for GPT-4 model.

    # Asynchronous method to create a new thread
    async def create_thread(self, messages: Optional[list] = None, metadata: Optional[dict] = None):
        thread = await self.client.beta.threads.create()
        return thread.id

    # Asynchronous method to retrieve a specific thread by its ID
    async def retrieve_thread(self, thread_id: str):
        return await self.client.beta.threads.retrieve(thread_id)

    # Asynchronous method to update a thread with new metadata
    async def update_thread(self, thread_id: str, metadata: dict):
        return await self.client.beta.threads.update(thread_id, metadata=metadata)

    # Asynchronous method to delete a specific thread by its ID
    async def delete_thread(self, thread_id: str):
        return await self.client.beta.threads.delete(thread_id)

    # Asynchronous method to create a message in a specific thread.
    async def create_message(self, thread_id: str, content: str, role: str = "user"):
        token_count = self.approximate_token_count(content)  # Getting the token count for the message.
        await self.client.beta.threads.messages.create(thread_id=thread_id, role=role, content=content)
        print(f"Tokens used in message: {token_count}")  # Printing the number of tokens used.



    # Asynchronous method to retrieve a specific message from a thread
    async def retrieve_message(self, thread_id: str, message_id: str):
        return await self.client.beta.threads.messages.retrieve(thread_id=thread_id, message_id=message_id)

    # Asynchronous method to list messages in a thread, with optional ordering and filtering
    async def list_messages(self, thread_id: str, order: str = 'desc', after: Optional[str] = None,
                            before: Optional[str] = None):
        try:
            return await self.client.beta.threads.messages.list(thread_id=thread_id,
                                                                order=order,
                                                                after=after,
                                                                before=before
                                                                )
        except Exception as e:
            print(f"An error occurred while retrieving messages: {e}")
            return None


    # Function to approximate the token count of a given text.
    # It uses the tiktoken encoder to tokenize the text and count the number of tokens.
    def approximate_token_count(self, text):
        tokens = self.encoder.encode(text)  # Encoding the text into tokens.
        token_count = len(tokens)  # Counting the number of tokens.
        return token_count


# Asynchronous main function demonstrating various operations with the thread manager
async def main():
    load_dotenv()  # Loading the API key from environment or .env file.
    api_key = os.getenv("OPENAI_API_KEY")  # Getting the API key from the environment variables.

    # Create an instance of the thread manager
    thread_manager = OpenAIThreadManager(api_key)

    # The following lines are examples of different operations. 
    # They are commented out, but you can uncomment them to use them.

    # Example operation - Create a new thread
    # new_thread_id = await thread_manager.create_thread()
    # print("ID of the new thread:", new_thread_id)

    # Example operation - Delete a specific thread
    # thread_id = "id_da_thread_aqui"  # Replace with the actual thread ID you want to delete
    # delete_response = await thread_manager.delete_thread(thread_id)
    # print("Delete response:", delete_response)

    # Example operation - Retrieve a specific thread
    # thread_id = "id_da_thread_aqui"  # Replace with the actual thread ID you want to retrieve
    # thread_details = await thread_manager.retrieve_thread(thread_id)
    # print("Details of the retrieved thread:", thread_details)

    # Example operation - Update an existing thread
    # thread_id = "id_da_thread_aqui"  # Replace with the actual thread ID you want to update
    # new_metadata = {"key": "value"}  # Replace with the new metadata you want to set
    # update_response = await thread_manager.update_thread(thread_id, new_metadata)
    # print("Update response:", update_response)

    # Example operation - Retrieve a specific message from a thread
    # thread_id = "id_da_thread_aqui"  # Replace with the actual thread ID
    # message_id = "id_da_mensagem_aqui"  # Replace with the actual message ID
    # message_details = await thread_manager.retrieve_message(thread_id, message_id)
    # print("Details of the retrieved message:", message_details)

    # Example operation - List messages from a specific thread
    # thread_id = "id_da_thread_aqui"  # Replace with the actual thread ID
    # messages = await thread_manager.list_messages(thread_id)
    # print("Messages from the thread:", messages)

    # Example operation - Create a new message in a specific thread
    # thread_id = "thread_NNt59EvjRSWuTeJkGBSg4jRX"  # Replace with the actual thread ID
    # content = "Test"  # Replace with the message content
    # message = await thread_manager.create_message(thread_id, content)
    # print("Created message:", message)

# Run the main function if this file is executed as a script
if __name__ == "__main__":
    asyncio.run(main())  # Running the main function asynchronously.
