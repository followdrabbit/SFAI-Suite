# Import necessary libraries
import asyncio  # For asynchronous programming
import datetime  # For handling date and time
import json  # For JSON operations
import os  # For operating system interactions, like file paths
from utils.thread_manager import OpenAIThreadManager  # Custom module for managing threads
from utils.text_replacer import replace_text_in_file  # Custom module for text replacement
from utils.asssistant_manager import OpenAIAssistantManager  # Custom module for managing OpenAI assistants
from utils.runs_manager import OpenAIRunsManager  # Custom module for managing OpenAI runs

# Constants for easier reference and maintenance
CLOUD_SECURITY_EXPERT = "Cloud Security Expert"
PRODUCT_NAME_PLACEHOLDER = "PRODUCT_NAME"
DATA_RAW_DIR = "data/raw"
DATA_STRUCTURED_DIR = "data/structured"

# Asynchronous function to find an assistant ID based on its name
async def find_assistant_id(assistant_manager, name):
    unique_assistants = await assistant_manager.list_assistants()
    return unique_assistants.get(name)

# Asynchronous function to create and process a run for a specific technology
async def create_and_process_run(thread_manager, runs_manager, technology, assistant_id, ticket):
    new_thread_id = await thread_manager.create_thread()
    new_prompt = replace_text_in_file('prompts/get_controls.txt', PRODUCT_NAME_PLACEHOLDER, technology)
    await thread_manager.create_message(new_thread_id, new_prompt)
    run_id = await runs_manager.create_run(new_thread_id, assistant_id)
    return await runs_manager.process_run(new_thread_id, run_id)

# Function to save raw and structured results into separate files
def save_results(result_raw, ticket):
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name_raw = os.path.join(DATA_RAW_DIR, f'{ticket}_controls_{current_time}_raw.txt')
    file_name_structured = os.path.join(DATA_STRUCTURED_DIR, f'{ticket}_controls_{current_time}_structured.txt')

    with open(file_name_raw, 'w', encoding='utf-8') as file:
        json.dump(result_raw, file, ensure_ascii=False, indent=4)

    assistant_message = next((item['message'] for item in result_raw if item['role'] == 'assistant'), None)
    if assistant_message:
        with open(file_name_structured, 'w', encoding='utf-8') as file:
            file.write(assistant_message)

    return file_name_raw, file_name_structured

# Main asynchronous function to create a baseline using the specified technology, API key, and ticket
async def create_baseline(technology, api_key, ticket):
    assistant_manager = OpenAIAssistantManager(api_key)
    assistant_id = await find_assistant_id(assistant_manager, CLOUD_SECURITY_EXPERT)

    if assistant_id is None:
        print("Assistant 'Cloud Security Expert' not found.")
        return

    thread_manager = OpenAIThreadManager(api_key)
    runs_manager = OpenAIRunsManager(api_key)

    result_raw = await create_and_process_run(thread_manager, runs_manager, technology, assistant_id, ticket)

    file_name_raw, file_name_structured = save_results(result_raw, ticket)
    print(f"Complete message saved in: {file_name_raw}")
    print(f"Assistant's message saved in: {file_name_structured}")
