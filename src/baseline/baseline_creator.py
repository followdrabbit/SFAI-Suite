# Imports
from utils.thread_manager import OpenAIThreadManager
from utils.text_replacer import replace_text_in_file
from utils.assistant_manager import OpenAIAssistantManager
from utils.runs_manager import OpenAIRunsManager

# Constants
CLOUD_SECURITY_EXPERT = "Cloud Security Expert"
PRODUCT_NAME_PLACEHOLDER = "PRODUCT_NAME"
CONTROL_NAME_PLACEHOLDER = "CONTROL_NAME"
DATA_RAW_DIR = "data/raw"
DATA_STRUCTURED_DIR = "data/structured"
GET_BASELINE_CONTROLS_PROMPT = 'prompts/get_baseline_controls.txt'
GET_BASELINE_AUDIT_PROMPT = 'prompts/get_baseline_audit.txt'
GET_BASELINE_REMEDIATION_PROMPT = 'prompts/get_baseline_remediation.txt'

async def find_assistant_id(assistant_manager, name):
    """Find assistant ID based on its name."""
    unique_assistants = await assistant_manager.list_assistants()
    return unique_assistants.get(name)

async def create_and_process_run(thread_manager, thread_id, runs_manager, assistant_id, prompt_file, placeholder, replacement_text):
    """Create and process a run for a specific placeholder replacement in a prompt."""
    new_prompt = replace_text_in_file(prompt_file, placeholder, replacement_text)
    await thread_manager.create_message(thread_id, new_prompt)
    run_id = await runs_manager.create_run(thread_id, assistant_id)
    return await runs_manager.process_run(thread_id, run_id)

def get_response(result_raw):
    """Extract assistant message from raw response."""
    assistant_message = next((item['message'] for item in result_raw if item['role'] == 'assistant'), None)
    return assistant_message or ""

async def process_control_block(thread_manager, thread_id, runs_manager, assistant_id, controls_extracted, prompt_file):
    """Process each control block in the extracted controls."""
    processed_data = []
    current_control_block = []

    for line in controls_extracted.strip().split('\n'):
        if line.strip():
            current_control_block.append(line.strip())
        else:
            if current_control_block:
                control_description = ' '.join(current_control_block)
                result = await create_and_process_run(thread_manager, thread_id, runs_manager, assistant_id, prompt_file, CONTROL_NAME_PLACEHOLDER, control_description)
                processed_data.append(result)
                current_control_block = []

    if current_control_block:
        control_description = ' '.join(current_control_block)
        result = await create_and_process_run(thread_manager, thread_id, runs_manager, assistant_id, prompt_file, CONTROL_NAME_PLACEHOLDER, control_description)
        processed_data.append(result)

    return processed_data


    return processed_data

async def create_baseline(technology, api_key, ticket):
    """Main function to create a baseline using specified technology, API key, and ticket."""
    assistant_manager = OpenAIAssistantManager(api_key)
    assistant_id = await find_assistant_id(assistant_manager, CLOUD_SECURITY_EXPERT)

    if assistant_id is None:
        print("Assistant 'Cloud Security Expert' not found.")
        return

    thread_manager = OpenAIThreadManager(api_key)
    runs_manager = OpenAIRunsManager(api_key)

    thread_id = await thread_manager.create_thread()
    controls_raw = await create_and_process_run(thread_manager, thread_id, runs_manager, assistant_id, GET_BASELINE_CONTROLS_PROMPT, PRODUCT_NAME_PLACEHOLDER, technology)
    controls_extracted = get_response(controls_raw)

    print(controls_extracted)
    print("\n" + "#" * 120 + "\n")

    audit_raw = await process_control_block(thread_manager, thread_id, runs_manager, assistant_id, controls_extracted, GET_BASELINE_AUDIT_PROMPT)
    remediation_raw = await process_control_block(thread_manager, thread_id, runs_manager, assistant_id, controls_extracted, GET_BASELINE_REMEDIATION_PROMPT)

    for result in audit_raw + remediation_raw:
        extracted_data = get_response(result)
        print(extracted_data)
        print("\n" + "#" * 120 + "\n")
