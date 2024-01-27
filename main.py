import asyncio
import os
import argparse
from dotenv import load_dotenv
from utils.asssistant_manager import OpenAIAssistantManager
from src.controls.controls_creator import create_baseline_request

async def main():
    # Load environment variables (API key) from the .env file
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key is None:
        print("Error: OPENAI_API_KEY not found. Please check your .env file.")
        return

    # Create an instance of the assistant manager with the API key
    manager = OpenAIAssistantManager(api_key)

    # Setup argparse for command line arguments
    parser = argparse.ArgumentParser(description='Calls controls_creator with technology and ticket parameters.')
    parser.add_argument('-tec', '--technology', type=str, required=True, help='The new technology name')
    # Uncomment and adjust as needed
    # parser.add_argument('-tic', '--ticket', type=str, required=True, help='The ticket associated with the change')
    
    # Parse the provided arguments
    args = parser.parse_args()

    # Call the list_assistants method and get the unique assistants
    unique_assistants = await manager.list_assistants()

    # Find the ID of the assistant named "Cloud Security Expert"
    assistant_id = None
    for name, id in unique_assistants.items():
        if name == "Cloud Security Expert":
            assistant_id = id
            break

    if assistant_id is None:
        print("Assistant 'Cloud Security Expert' not found.")
        return

    # Call the controls_creator function with the technology and the assistant ID
    create_baseline_request(technology=args.technology, assistant_id=assistant_id)

if __name__ == "__main__":
    asyncio.run(main())
