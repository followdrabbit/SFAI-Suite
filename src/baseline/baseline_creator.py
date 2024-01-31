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
async def create_run(thread_manager, thread_id, runs_manager, technology, assistant_id, prompt):
    new_prompt = replace_text_in_file(prompt, PRODUCT_NAME_PLACEHOLDER, technology)
    await thread_manager.create_message(thread_id, new_prompt)
    run_id = await runs_manager.create_run(thread_id, assistant_id)
    return await runs_manager.process_run(thread_id, run_id)


# Asynchronous function to create and process a run for a specific technology
async def process_run(thread_manager, thread_id, runs_manager, assistant_id, prompt, CONTROL_NAME, control_description):
    new_prompt = replace_text_in_file(prompt, CONTROL_NAME, control_description)
    await thread_manager.create_message(thread_id, new_prompt)
    run_id = await runs_manager.create_run(thread_id, assistant_id)
    return await runs_manager.process_run(thread_id, run_id)

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


def get_response(result_raw):
    extract_data = ""
    raw_data = json.dumps(result_raw, ensure_ascii=False, indent=4)  # Alterado para json.dumps
    assistant_message = next((item['message'] for item in result_raw if item['role'] == 'assistant'), None)
    if assistant_message:
        extract_data += assistant_message

    return extract_data

def extract_full_control_description(line):
    # Separa o número do controle e o resto do texto
    control_number, control_text = line.split('.', 1)
    return control_text.strip()


# Main asynchronous function to create a baseline using the specified technology, API key, and ticket
async def create_baseline(technology, api_key, ticket):
    assistant_manager = OpenAIAssistantManager(api_key)
    assistant_id = await find_assistant_id(assistant_manager, CLOUD_SECURITY_EXPERT)

    if assistant_id is None:
        print("Assistant 'Cloud Security Expert' not found.")
        return

    thread_manager = OpenAIThreadManager(api_key)
    runs_manager = OpenAIRunsManager(api_key)

    thread_id = await thread_manager.create_thread()
    controls_raw = await create_run(thread_manager, thread_id, runs_manager, technology, assistant_id, 'prompts/get_baseline_controls.txt')
    controls_extracted = get_response(controls_raw)
    print (controls_extracted)

    print("")
    print ("############################################################################################################")
    print("")

    audit_raw = []  # Supondo que seja uma lista


    # Variável para armazenar o bloco atual de descrição de controle
    current_control_block = []

    for line in controls_extracted.strip().split('\n'):
        if line.strip():
            # Adiciona a linha atual ao bloco de controle atual
            current_control_block.append(line.strip())
        else:
            # Verifica se há um bloco de controle para processar
            if current_control_block:
                # Junta todas as linhas do bloco de controle em uma única descrição
                control_description = ' '.join(current_control_block)

                print(f"Processando controle: {control_description}")

                # Chame a função process_run com a descrição completa do controle
                result = await process_run(thread_manager, thread_id, runs_manager, assistant_id, 'prompts/get_baseline_audit.txt', "CONTROL_NAME", control_description)
                audit_raw.append(result)
                # Resto do seu código...

            # Reseta o bloco de controle para o próximo
            current_control_block = []

    # Verifica se há um último bloco de controle após o loop
    if current_control_block:
        control_description = ' '.join(current_control_block)

        print(f"Processando controle: {control_description}")
        # Chame a função process_run com a descrição completa do controle
        result = await process_run(thread_manager, thread_id, runs_manager, assistant_id, 'prompts/get_baseline_audit.txt', "CONTROL_NAME", control_description)
        audit_raw.append(result)

        

    # # Dividindo o texto em linhas e processando cada linha
    # for line in controls_extracted.strip().split('\n'):
    #     if line.strip():  # Verificando se a linha não está vazia
    #         control_description = line.split(': ', 1)[1] if ': ' in line else line
    #         print(f"Processando controle: {control_description}")

    #         # Agora estamos adicionando o resultado a uma lista
    #         result = await process_run(thread_manager, thread_id, runs_manager, assistant_id, 'prompts/get_baseline_audit.txt', "CONTROL_NAME", control_description)
    #         audit_raw.append(result)

    # Processar audit_raw como necessário
    # Por exemplo, se você quer extrair uma resposta de cada resultado:
    for result in audit_raw:
        audit_extracted = get_response(result)
        print("")
        print ("############################################################################################################")
        print("")
        print(audit_extracted)

    #file_name_raw, file_name_structured = save_results(controls_raw, ticket)
    #print(f"Complete message saved in: {file_name_raw}")
    #print(f"Assistant's message saved in: {file_name_structured}")



   #result_raw = await create_and_process_run(thread_manager, runs_manager, technology, assistant_id, ticket)