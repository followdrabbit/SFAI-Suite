# Imports corrigidos conforme os nomes fornecidos originalmente
import json
import os
from utils.thread_manager import OpenAIThreadManager
from utils.assistant_manager import OpenAIAssistantManager
from utils.runs_manager import OpenAIRunsManager
from utils.text_replacer import replace_text_in_file

# Constantes
CLOUD_SECURITY_EXPERT = "Cloud Security Expert"
PRODUCT_NAME_PLACEHOLDER = "PRODUCT_NAME"
CONTROL_NAME_PLACEHOLDER = "CONTROL_NAME"
DATA_RAW_DIR = "data/raw"
DATA_STRUCTURED_DIR = "data/structured"
GET_BASELINE_CONTROLS_PROMPT = 'prompts/get_baseline_controls.txt'
BASELINE_AUDIT_PROMPT = 'prompts/get_baseline_audit.txt'
BASELINE_REMEDIATION_PROMPT = 'prompts/get_baseline_remediation.txt'
BASELINE_REFERENCE_PROMPT = 'prompts/get_baseline_reference.txt'

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
    """Processes control blocks for audit and remediation."""
    all_controls = {}
    for prompt_file, process in [(BASELINE_AUDIT_PROMPT, 'Audit'), (BASELINE_REMEDIATION_PROMPT, 'Remediation'), (BASELINE_REFERENCE_PROMPT, 'Reference')]:
        controls, control_counter = {}, 1
        current_control_block, last_processed_block = [], None
        for line in controls_extracted.strip().split('\n'):
            if line.strip():
                current_control_block.append(line.strip())
            else:
                if current_control_block and current_control_block != last_processed_block:
                    # Processa o bloco de controle atual
                    control_description = ' '.join(current_control_block)
                    control_key = f"Control{control_counter}"
                    response = await create_and_process_run(thread_manager, thread_id, runs_manager, assistant_id, prompt_file, CONTROL_NAME_PLACEHOLDER, control_description, process)
                    result = next((item['message'] for item in response if item['role'] == 'assistant'), None)
                    if result:
                        controls[control_key] = {"Description": control_description, process: result}
                        control_counter += 1
                    last_processed_block = current_control_block.copy()
                    current_control_block = []

        # Processa o último bloco de controle se ele não foi processado
        if current_control_block and current_control_block != last_processed_block:
            control_description = ' '.join(current_control_block)
            control_key = f"Control{control_counter}"
            response = await create_and_process_run(thread_manager, thread_id, runs_manager, assistant_id, prompt_file, CONTROL_NAME_PLACEHOLDER, control_description, process)
            result = next((item['message'] for item in response if item['role'] == 'assistant'), None)
            if result:
                controls[control_key] = {"Description": control_description, process: result}
        
        all_controls[process] = controls
    return all_controls

def save_data(data, ticket, base_dir="data/raw/baseline"):
    """
    Tenta salvar os dados em um arquivo JSON no diretório especificado.
    Verifica se o arquivo foi salvo com sucesso e lida com possíveis erros.

    Args:
    - data: Os dados a serem salvos (dicionário).
    - ticket: Identificador único para os dados.
    - base_dir: Diretório base onde os dados serão salvos.
    """
    try:
        
        # Define o caminho completo do arquivo
        file_path = os.path.join(base_dir, f"{ticket}.json")
        
        # Salva os dados no arquivo JSON
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        
        # Verifica se o arquivo foi de fato criado
        if os.path.exists(file_path):
            print(f"Dados salvos com sucesso em: {file_path}")
        else:
            # Isso não deveria acontecer a menos que o arquivo seja deletado
            # ou movido após ser criado mas antes desta verificação
            print("O arquivo não foi encontrado após a tentativa de salvamento.")
    except Exception as e:
        # Captura qualquer exceção que possa ocorrer e exibe a mensagem de erro
        print(f"Ocorreu um erro ao tentar salvar os dados: {e}")

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

    save_data(processed_controls, ticket)
