# Imports corrigidos conforme os nomes fornecidos originalmente
import json
import os
import re
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from utils.thread_manager import OpenAIThreadManager
from utils.assistant_manager import OpenAIAssistantManager
from utils.runs_manager import OpenAIRunsManager
from utils.text_replacer import replace_text_in_file


# Constantes
CLOUD_SECURITY_EXPERT = "Cloud Security Expert"
PRODUCT_NAME_PLACEHOLDER = "PRODUCT_NAME"
CONTROL_NAME_PLACEHOLDER = "CONTROL_NAME"
DATA_RAW_DIR = "data/raw"
DATA_STRUCTURED_DIR = "data/structured/"
DATA_STRUCTURED_BASELINE_DIR = "data/structured/baseline"
GET_BASELINE_CONTROLS_PROMPT = 'prompts/get_baseline_controls.txt'
BASELINE_AUDIT_PROMPT = 'prompts/get_baseline_audit.txt'
BASELINE_REMEDIATION_PROMPT = 'prompts/get_baseline_remediation.txt'
BASELINE_REFERENCE_PROMPT = 'prompts/get_baseline_reference.txt'
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
TEMPLATE_DIR = 'templates'



# Caminho para o arquivo HTML de saída
output_file_path = 'caminho/para/o/arquivo/de/saida.html'

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


def save_data(data, ticket, technology, base_dir=DATA_STRUCTURED_BASELINE_DIR):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    file_path = os.path.join(base_dir, f"{ticket}_{technology}_{timestamp}.json")
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {file_path}")

import pandas as pd
import re
from jinja2 import Environment, FileSystemLoader

def generate_html_from_processed_controls(processed_controls: dict, template_dir: str, output_file_path: str) -> None:
    """
    Gera um arquivo HTML a partir de dados de controle fornecidos como um dicionário JSON,
    utilizando um template HTML do Jinja2.

    Args:
        processed_controls (dict): Dicionário contendo os dados de controle, incluindo 'Controls', 'Audits', e 'Remediations'.
        template_dir (str): O diretório onde o template Jinja2 está localizado.
        output_file_path (str): O caminho para o arquivo HTML de saída que será gerado.

    Returns:
        None: A função não retorna nada, mas gera um arquivo HTML.
    """
    rows = []
    for control_id, control_text in processed_controls.get('Controls', {}).items():
        control_match = re.search(r"CONTROL: (.*?)\s*(RATIONALE:|$)", control_text)
        rationale_match = re.search(r"RATIONALE: (.*?)\s*(REFERENCE:|$)", control_text)

        control = control_match.group(1).strip() if control_match else "N/A"
        rationale = rationale_match.group(1).strip() if rationale_match else "N/A"
        audit = processed_controls['Audits'].get(control_id.replace('Control', 'Audit'), "N/A")
        remediation = processed_controls['Remediations'].get(control_id.replace('Control', 'Remediation'), "N/A")

        rows.append({
            'ControlID': control_id,
            'Control': control,
            'Rationale': rationale,
            'Audit': audit,
            'Remediation': remediation
        })

    # Cria o DataFrame
    df = pd.DataFrame(rows)

    # Configura o Jinja2 para carregar o template
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('template_baseline.html')

    # Renderiza o template com os dados
    html_output = template.render(rows=df.to_dict(orient='records'))

    # Salva o HTML renderizado em um arquivo
    with open(output_file_path, 'w') as file:
        file.write(html_output)

    print(f"HTML gerado com sucesso e salvo em '{output_file_path}'.")

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

    # save controls Raw Json
    save_data(controls_raw, ticket, technology, DATA_RAW_DIR)

    # save extracted controls txt
    file_path = os.path.join(DATA_STRUCTURED_DIR, f"{ticket}_{technology}_{timestamp}.txt")
    with open(file_path, 'w') as file:
        file.write(controls_extracted)
    
    print(f"Data saved to {file_path}")

    # processed_controls = await process_control_blocks(thread_manager, thread_id, runs_manager, assistant_id, controls_extracted)
    # print(processed_controls)

    # save_data(processed_controls, ticket, technology)

    # output_file_path = f'data/baseline/{ticket}_{technology}_{timestamp}.html'
    # generate_html_from_processed_controls(processed_controls, TEMPLATE_DIR, output_file_path)

    # # Preparando os dados para o DataFrame
    # rows = []
    # for control_id, control_text in processed_controls['Controls'].items():
    #     control_info = control_text.split(". ")
    #     control = control_info[0].split("CONTROL: ")[1]
    #     rationale = control_info[1].split("RATIONALE: ")[1]
    #     audit = processed_controls['Audits'][control_id.replace('Control', 'Audit')]
    #     remediation = processed_controls['Remediations'][control_id.replace('Control', 'Remediation')]
    #     rows.append({
    #         'ControlID': control_id,
    #         'Control': control,
    #         'Rational': rationale,
    #         'Audit': audit,
    #         'Remediation': remediation
    #     })

    # # Convertendo para DataFrame
    # df = pd.DataFrame(rows)

    # # Configuração do Jinja2 para carregar o template do diretório 'templates'
    # env = Environment(loader=FileSystemLoader('templates'))

    # # Carregando o template chamado 'template_baseline.html'
    # template = env.get_template('template_baseline.html')

    # # Renderizando o template com os dados do DataFrame
    # html_output = template.render(rows=df.to_dict(orient='records'))

    # # Salvando o HTML renderizado em um arquivo
    # output_file_path = f'data/baseline/{ticket}_{technology}_{timestamp}.html'
    # with open(output_file_path, 'w') as file:
    #     file.write(html_output)

    # print(f"HTML gerado com sucesso e salvo em '{output_file_path}'.")