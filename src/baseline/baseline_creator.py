# Imports corrigidos conforme os nomes fornecidos originalmente
import json
import os
from datetime import datetime
from utils.thread_manager import OpenAIThreadManager
from utils.assistant_manager import OpenAIAssistantManager
from utils.runs_manager import OpenAIRunsManager
from utils.text_replacer import replace_text_in_file

# Constantes
CLOUD_SECURITY_EXPERT = "Cloud Security Expert"
PRODUCT_NAME_PLACEHOLDER = "PRODUCT_NAME"
CONTROL_NAME_PLACEHOLDER = "CONTROL_NAME"
DATA_STRUCTURED_DIR = "data/structured/baseline"
GET_BASELINE_CONTROLS_PROMPT = 'prompts/get_baseline_controls.txt'
BASELINE_AUDIT_PROMPT = 'prompts/get_baseline_audit.txt'
BASELINE_REMEDIATION_PROMPT = 'prompts/get_baseline_remediation.txt'
BASELINE_REFERENCE_PROMPT = 'prompts/get_baseline_reference.txt'
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

async def find_assistant_id(assistant_manager, name):
    """Returns the ID of an assistant by name."""
    unique_assistants = await assistant_manager.list_assistants()
    return unique_assistants.get(name)

async def create_and_process_run(thread_manager, thread_id, runs_manager, assistant_id, prompt_file, placeholder, replacement_text, process):
    """Creates and processes a run for replacing placeholders in a prompt."""
    new_prompt = replace_text_in_file(prompt_file, placeholder, replacement_text)
    print(f"Getting {process} for: {replacement_text}")
    await thread_manager.create_message(thread_id, new_prompt)
    run_id = await runs_manager.create_run(thread_id, assistant_id)
    return await runs_manager.process_run(thread_id, run_id)

def extract_response(result_raw):
    """Extracts assistant messages from the raw response."""
    messages = []
    for item in (item for sublist in result_raw for item in (sublist if isinstance(sublist, list) else [sublist])):
        if item.get('role') == 'assistant':
            messages.append(item.get('message', ''))
    return " ".join(messages)


async def process_control_blocks(thread_manager, thread_id, runs_manager, assistant_id, controls_extracted):
    processed_controls = {'Controls': {}, 'Audits': {}, 'Remediations': {}, 'References': {}}
    control_counter = 1

    for control_description in controls_extracted.split('\n\n'):
        control_key = f"Control{control_counter}"
        audit_key = f"Audit{control_counter}"
        remediation_key = f"Remediation{control_counter}"
        reference_key = f"Reference{control_counter}"

        # Processo de criação e execução para 'Audit'
        audit_response = await create_and_process_run(thread_manager, thread_id, runs_manager, assistant_id, BASELINE_AUDIT_PROMPT, CONTROL_NAME_PLACEHOLDER, control_description, "Audit")
        audit_result = next((item['message'] for item in audit_response if item['role'] == 'assistant'), None)
        if audit_result:
            processed_controls['Audits'][audit_key] = audit_result

        # Processo de criação e execução para 'Remediation'
        remediation_response = await create_and_process_run(thread_manager, thread_id, runs_manager, assistant_id, BASELINE_REMEDIATION_PROMPT, CONTROL_NAME_PLACEHOLDER, control_description, "Remediation")
        remediation_result = next((item['message'] for item in remediation_response if item['role'] == 'assistant'), None)
        if remediation_result:
            processed_controls['Remediations'][remediation_key] = remediation_result

        # Processo de criação e execução para 'Reference'
        reference_response = await create_and_process_run(thread_manager, thread_id, runs_manager, assistant_id, BASELINE_REFERENCE_PROMPT, CONTROL_NAME_PLACEHOLDER, control_description, "Reference")
        reference_result = next((item['message'] for item in reference_response if item['role'] == 'assistant'), None)
        if reference_result:
            processed_controls['References'][reference_key] = reference_result

        # Sempre adiciona a descrição do controle, independentemente dos resultados das outras chamadas
        processed_controls['Controls'][control_key] = control_description

        control_counter += 1

    return processed_controls


def save_data(data, ticket, technology, base_dir=DATA_STRUCTURED_DIR):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    file_path = os.path.join(base_dir, f"{ticket}_{technology}_{timestamp}.json")
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {file_path}")


async def create_baseline(technology, api_key, ticket):
    """Main function to create a baseline for a given technology."""
    assistant_manager = OpenAIAssistantManager(api_key)
    assistant_id = await find_assistant_id(assistant_manager, CLOUD_SECURITY_EXPERT)
    if assistant_id is None:
        print("Assistant 'Cloud Security Expert' not found.")
        return

    thread_manager, runs_manager = OpenAIThreadManager(api_key), OpenAIRunsManager(api_key)
    thread_id = await thread_manager.create_thread()
    controls_raw = await create_and_process_run(thread_manager, thread_id, runs_manager, assistant_id, GET_BASELINE_CONTROLS_PROMPT, PRODUCT_NAME_PLACEHOLDER, technology, "Controls")
    controls_extracted = extract_response(controls_raw)

    print("##################################################################")
    print(controls_extracted)
    print("##################################################################")

    processed_controls = await process_control_blocks(thread_manager, thread_id, runs_manager, assistant_id, controls_extracted)
    print(processed_controls)

    save_data(processed_controls, ticket, technology)
