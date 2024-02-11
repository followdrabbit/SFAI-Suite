import openai
import asyncio
import os
from typing import Optional
from dotenv import load_dotenv

class OpenAIAssistantManager:
    def __init__(self, api_key):
        # Initialize the manager with an asynchronous OpenAI client.
        # The client is used for interacting with the OpenAI API.
        self.client = openai.AsyncClient(api_key=api_key)

    async def list_assistants(self):
        # Asynchronously fetch the list of assistants from the OpenAI API.
        response = await self.client.beta.assistants.list()
        # unique_assistants = {}
        # for assistant in response.data:
        #     # Check for duplicate assistants based on their names.
        #     if assistant.name not in unique_assistants:
        #         unique_assistants[assistant.name] = assistant.id
        #     else:
        #         # Print a message and delete the duplicate assistant.
        #         print(f"Duplicate assistant found: {assistant.name} with ID {assistant.id} - Removing.")
        #         await self.delete_assistant(assistant.id)
        return response

    async def delete_assistant(self, assistant_id: str):
        # Delete an assistant using its ID.
        try:
            return await self.client.beta.assistants.delete(assistant_id)
        except openai.NotFoundError as e:
            print(f"Error deleting assistant {assistant_id}: {e}")

    async def create_assistant(self, name, instructions, tools, model):
        try:
            # Asynchronously create a new assistant.
            assistant = await self.client.beta.assistants.create(
                name=name,
                instructions=instructions,
                tools=tools,
                model=model
            )
            return (assistant.id)
        except Exception as e:
            print(f"Error creating assistant: {e}")

    async def update_assistant(self, assistant_id: str, name: Optional[str] = None, 
                               description: Optional[str] = None,
                               instructions: Optional[str] = None, 
                               tools: Optional[list] = None):
        # Update specified fields of an assistant.
        update_fields = {}
        # Add provided fields to the update request.
        if name is not None:
            update_fields['name'] = name
        if description is not None:
            update_fields['description'] = description
        if instructions is not None:
            update_fields['instructions'] = instructions
        if tools is not None:
            update_fields['tools'] = tools
        try:
            # Perform the update operation asynchronously.
            return await self.client.beta.assistants.update(assistant_id, **update_fields)
        except Exception as e:
            print(f"Error updating assistant: {e}")

    async def create_assistant_file(self, assistant_id: str, file_id: str):
        # Create a file association with an assistant asynchronously.
        # 'assistant_id' is the ID of the assistant, and 'file_id' is the ID of the file to be associated.
        return await self.client.beta.assistants.files.create(assistant_id=assistant_id, file_id=file_id)

    async def delete_assistant_file(self, assistant_id: str, file_id: str):
        # Delete a file association from an assistant asynchronously.
        # 'assistant_id' is the ID of the assistant, and 'file_id' is the ID of the file to be disassociated.
        return await self.client.beta.assistants.files.delete(assistant_id, file_id)

    async def list_assistant_files(self, assistant_id: str):
        # List all files associated with an assistant asynchronously.
        # 'assistant_id' is the ID of the assistant whose files are to be listed.
        return await self.client.beta.assistants.files.list(assistant_id)

    async def retrieve_assistant(self, assistant_id: str):
        # Retrieve the details of a specific assistant asynchronously.
        # 'assistant_id' is the ID of the assistant to be retrieved.
        # This method returns the detailed information of the specified assistant.
        return await self.client.beta.assistants.retrieve(assistant_id)


async def main():
    # Load environment variables (API key) from the .env file.
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key is None:
        print("Error: OPENAI_API_KEY not found. Please check your .env file.")
        return

    # Initialize the assistant manager with the API key.
    manager = OpenAIAssistantManager(api_key)

    # Create a new assistant (example).
    await manager.create_assistant(
        name="Cloud Security Expert",
        instructions="An assistant specialized in providing customized security recommendations for a wide range of AWS products. It should analyze the configuration and usage of each product, identify potential vulnerabilities, and recommend specific security controls, aligned with information security best practices, relevant compliance standards, and security frameworks. The assistant should offer guidance for continuous monitoring and incident response, relying on services like CloudWatch and AWS Security Hub, and stay updated on the latest security threats and vulnerabilities.",
        tools=[{"type": "code_interpreter"}],
        model="gpt-3.5-turbo-16k"
    )

    # Update an assistant's name (example).
    # Replace 'assistant_id_here' with the actual assistant's ID.
    #assistant_id_to_update = "assistant_id_here"
    #await manager.update_assistant(assistant_id_to_update, name="New Assistant Name")

    # Fetch and print the list of unique assistants.
    unique_assistants = await manager.list_assistants()
    for name, id in unique_assistants.items():
        print(f"Name: {name}, ID: {id}")
    
    # Example usage of retrieve_assistant
    #assistant_id = "assistant_id_here"  # Replace with the actual assistant's ID
    #assistant_details = await manager.retrieve_assistant(assistant_id)
    #print(assistant_details)

if __name__ == "__main__":
    asyncio.run(main())
