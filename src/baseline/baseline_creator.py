# Imports
from utils.thread_manager import OpenAIThreadManager  # Importing OpenAIThreadManager for thread management.
from utils.text_replacer import replace_text_in_file  # Importing function to replace text in files.
from utils.assistant_manager import OpenAIAssistantManager  # Importing OpenAIAssistantManager for managing assistants.
from utils.runs_manager import OpenAIRunsManager  # Importing OpenAIRunsManager for managing runs.

# Constants
CLOUD_SECURITY_EXPERT = "Cloud Security Expert"  # Constant for a specific assistant role.
PRODUCT_NAME_PLACEHOLDER = "PRODUCT_NAME"  # Placeholder for product name in prompts.
CONTROL_NAME_PLACEHOLDER = "CONTROL_NAME"  # Placeholder for control name in prompts.
DATA_RAW_DIR = "data/raw"  # Directory path for raw data.
DATA_STRUCTURED_DIR = "data/structured"  # Directory path for structured data.
GET_BASELINE_CONTROLS_PROMPT = 'prompts/get_baseline_controls.txt'  # File path for baseline controls prompt.


async def find_assistant_id(assistant_manager, name):
    """Find assistant ID based on its name. This is an asynchronous function."""
    unique_assistants = await assistant_manager.list_assistants()  # List all assistants.
    return unique_assistants.get(name)  # Return the ID of the assistant with the given name.

async def create_and_process_run(thread_manager, thread_id, runs_manager, assistant_id, prompt_file, placeholder, replacement_text):
    """Create and process a run for a specific placeholder replacement in a prompt. This is an asynchronous function."""
    new_prompt = replace_text_in_file(prompt_file, placeholder, replacement_text)  # Replace placeholder in prompt file.
    print("Getting controls")
    await thread_manager.create_message(thread_id, new_prompt)  # Create a message in the thread.
    run_id = await runs_manager.create_run(thread_id, assistant_id)  # Create a run with the thread ID and assistant ID.
    return await runs_manager.process_run(thread_id, run_id)  # Process the run and return the result.

def extract_response(result_raw):
    """
    Extract assistant messages from the raw response.

    Args:
    result_raw (list): A list or a list of lists containing dictionaries with 'role' and 'message' keys.

    Returns:
    str: A concatenated string of all assistant messages.
    """
    messages = []

    try:
        # Check if result_raw is a list of lists or a simple list
        if result_raw and isinstance(result_raw[0], list):
            # It's a list of lists: iterate over each sublist
            for sublist in result_raw:
                # Iterate over each item (dictionary) in the sublist
                for item in sublist:
                    # Check if the item is a dictionary and the role is 'assistant'
                    if isinstance(item, dict) and item.get('role') == 'assistant':
                        # Append the message of the assistant to the messages list
                        messages.append(item.get('message', ''))
        else:
            # It's a simple list: iterate directly over result_raw
            for item in result_raw:
                # Check if the item is a dictionary and the role is 'assistant'
                if isinstance(item, dict) and item.get('role') == 'assistant':
                    # Append the message of the assistant to the messages list
                    messages.append(item.get('message', ''))

    except Exception as e:
        # Print an error message if an exception occurs
        print(f"An error occurred while processing the response: {e}")
        # Optional: Return an error message or an empty list depending on how you want to handle errors
        # return "Error processing response"
        # or
        # return []

    # Join all messages in the list into a single string separated by spaces
    return " ".join(messages)

async def process_control_blocks(thread_manager, thread_id, runs_manager, assistant_id, controls_extracted):
    all_controls = {}
    prompt_files = ['prompts/get_baseline_audit.txt', 'prompts/get_baseline_remediation.txt']
    for prompt_file in prompt_files:  # Itera sobre a lista de valores prompt_file
        # Define o valor de 'process' com base em 'prompt_file'
        if prompt_file == 'prompts/get_baseline_audit.txt':
            process = 'Audit'
        elif prompt_file == 'prompts/get_baseline_remediation.txt':
            process = 'Remediation'
        controls = {}
        control_counter = 1
        current_control_block = []
        last_processed_block = None

        for line in controls_extracted.strip().split('\n'):
            if line.strip():
                current_control_block.append(line.strip())
            else:
                if current_control_block and current_control_block != last_processed_block:
                    control_description = ' '.join(current_control_block)
                    print(f"Getting {process} for block: {control_description}")
                    control_key = f"Control{control_counter}"
                    controls[control_key] = {
                        "Description": control_description,
                    }
                    response = await create_and_process_run(thread_manager, thread_id, runs_manager, assistant_id, prompt_file, CONTROL_NAME_PLACEHOLDER, control_description)
                    result = next((item['message'] for item in response if item['role'] == 'assistant' and 'message' in item), None)
                    if result:
                        print(result)
                        controls[control_key][process] = result
                        control_counter += 1
                    last_processed_block = current_control_block.copy()
                    current_control_block = []

        if current_control_block and current_control_block != last_processed_block:
            control_description = ' '.join(current_control_block)
            print(f"Getting {process} for block: {control_description}")
            response = await create_and_process_run(thread_manager, thread_id, runs_manager, assistant_id, prompt_file, CONTROL_NAME_PLACEHOLDER, control_description)
            result = next((item['message'] for item in response if item['role'] == 'assistant' and 'message' in item), None)
            if result:
                print(result)
                control_key = f"Control{control_counter}"
                controls[control_key] = {
                    "Description": control_description,
                }
                controls[control_key][process] = result
                control_counter += 1

        all_controls[prompt_file] = controls  # Armazena os controles para cada prompt_file

    return all_controls




async def create_baseline(technology, api_key, ticket):
    """Main function to create a baseline using specified technology, API key, and ticket. This is an asynchronous function."""
    assistant_manager = OpenAIAssistantManager(api_key)  # Initialize the assistant manager with the API key.
    assistant_id = await find_assistant_id(assistant_manager, CLOUD_SECURITY_EXPERT)  # Find the ID of the Cloud Security Expert.

    # Check if the assistant ID was found, if not, print a message and return.
    if assistant_id is None:
        print("Assistant 'Cloud Security Expert' not found.")
        return

    thread_manager = OpenAIThreadManager(api_key)  # Initialize the thread manager with the API key.
    runs_manager = OpenAIRunsManager(api_key)  # Initialize the runs manager with the API key.

    thread_id = await thread_manager.create_thread()  # Create a new thread.
    controls_raw = await create_and_process_run(thread_manager, thread_id, runs_manager, assistant_id, GET_BASELINE_CONTROLS_PROMPT, PRODUCT_NAME_PLACEHOLDER, technology)
    controls_extracted = extract_response(controls_raw)  # Extract controls from the raw response.

    # Process audit for the extracted controls.
    #Teste = await process_control_block(thread_manager, thread_id, runs_manager, assistant_id, controls_extracted, GET_BASELINE_AUDIT_PROMPT, "audit")
    # Para usar a função modificada:
    Teste = await process_control_blocks(thread_manager, thread_id, runs_manager, assistant_id, controls_extracted)
    print("#####################################################################")
    print("#####################################################################")
    print("#####################################################################")
    print(Teste)
    # Process remediation for the extracted controls.
    #Teste = await process_control_block(thread_manager, thread_id, runs_manager, assistant_id, controls_extracted, GET_BASELINE_REMEDIATION_PROMPT, "remediation")


    # response = await thread_manager.list_messages(thread_id)
    # for message in reversed(response.data):
    #     print(message.content[0].text.value)
    #     print()
    #     print()

