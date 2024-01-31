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
GET_BASELINE_AUDIT_PROMPT = 'prompts/get_baseline_audit.txt'  # File path for baseline audit prompt.
GET_BASELINE_REMEDIATION_PROMPT = 'prompts/get_baseline_remediation.txt'  # File path for baseline remediation prompt.

async def find_assistant_id(assistant_manager, name):
    """Find assistant ID based on its name. This is an asynchronous function."""
    unique_assistants = await assistant_manager.list_assistants()  # List all assistants.
    return unique_assistants.get(name)  # Return the ID of the assistant with the given name.

async def create_and_process_run(thread_manager, thread_id, runs_manager, assistant_id, prompt_file, placeholder, replacement_text):
    """Create and process a run for a specific placeholder replacement in a prompt. This is an asynchronous function."""
    new_prompt = replace_text_in_file(prompt_file, placeholder, replacement_text)  # Replace placeholder in prompt file.
    await thread_manager.create_message(thread_id, new_prompt)  # Create a message in the thread.
    run_id = await runs_manager.create_run(thread_id, assistant_id)  # Create a run with the thread ID and assistant ID.
    return await runs_manager.process_run(thread_id, run_id)  # Process the run and return the result.

def get_response(result_raw):
    """Extract assistant message from raw response."""
    assistant_message = next((item['message'] for item in result_raw if item['role'] == 'assistant'), None)  # Find the assistant's message.
    return assistant_message or ""  # Return the assistant's message or an empty string if not found.

async def process_control_block(thread_manager, thread_id, runs_manager, assistant_id, controls_extracted, prompt_file):
    """Process each control block in the extracted controls. This is an asynchronous function."""
    processed_data = []  # List to store processed data.
    current_control_block = []  # Temporary storage for the current control block.

    # Loop through each line in the extracted controls.
    for line in controls_extracted.strip().split('\n'):
        if line.strip():  # If the line is not empty.
            current_control_block.append(line.strip())  # Add the line to the current control block.
        else:
            # Process the current control block if it's not empty.
            if current_control_block:
                control_description = ' '.join(current_control_block)  # Join all lines in the control block.
                result = await create_and_process_run(thread_manager, thread_id, runs_manager, assistant_id, prompt_file, CONTROL_NAME_PLACEHOLDER, control_description)
                processed_data.append(result)  # Append the result to processed data.
                current_control_block = []  # Reset the current control block.

    # Process the last control block if it's not empty.
    if current_control_block:
        control_description = ' '.join(current_control_block)
        result = await create_and_process_run(thread_manager, thread_id, runs_manager, assistant_id, prompt_file, CONTROL_NAME_PLACEHOLDER, control_description)
        processed_data.append(result)

    return processed_data

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
    controls_extracted = get_response(controls_raw)  # Extract controls from the raw response.

    print(controls_extracted)  # Print the extracted controls information.
    print("\n" + "#" * 120 + "\n")  # Print a separator line consisting of 120 hash (#) characters for visual separation in the output.


    # Process audit and remediation for the extracted controls.
    audit_raw = await process_control_block(thread_manager, thread_id, runs_manager, assistant_id, controls_extracted, GET_BASELINE_AUDIT_PROMPT)
    remediation_raw = await process_control_block(thread_manager, thread_id, runs_manager, assistant_id, controls_extracted, GET_BASELINE_REMEDIATION_PROMPT)

    # Print the results of the audit and remediation processes.
    for result in audit_raw + remediation_raw:
        extracted_data = get_response(result)
        print(extracted_data)
        print("\n" + "#" * 120 + "\n")
