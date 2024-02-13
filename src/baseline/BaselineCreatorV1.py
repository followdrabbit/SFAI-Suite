# Imports corrigidos conforme os nomes fornecidos originalmente
import json
import os
import re
import pandas as pd
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from utils.thread_manager import OpenAIThreadManager
from utils.assistant_manager import OpenAIAssistantManager
from utils.runs_manager import OpenAIRunsManager
from utils.text_replacer import replace_text_in_file


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Constantes
PRODUCT_NAME_PLACEHOLDER = "PRODUCT_NAME"
CONTROL_NAME_PLACEHOLDER = "CONTROL_NAME"
DATA_STRUCTURED_DIR = "data/structured/"
GET_BASELINE_CONTROLS_PROMPT = 'prompts/BaselineCreatorGetControls.txt'
BASELINE_AUDIT_PROMPT = 'prompts/BaselineCreatorGetAudit.txt'
BASELINE_REMEDIATION_PROMPT = 'prompts/BaselineCreatorGetRemediation.txt'
BASELINE_REFERENCE_PROMPT = 'prompts/BaselineCreatorGetReference.txt'
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
TEMPLATE_DIR = 'templates'
api_key = os.getenv("OPENAI_API_KEY")
BASELINESECURITYEXPERT_ID = os.getenv("BASELINESECURITYEXPERT_ID")
SECURITYGUARDIANAI_ID = os.getenv("SECURITYGUARDIANAI_ID")



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

import re
from jinja2 import Environment, FileSystemLoader
import pandas as pd

from jinja2 import Environment, FileSystemLoader

def generate_html_from_processed_controls(processed_controls: dict, template_dir: str, output_file_path: str) -> None:
    """
    Gera um arquivo HTML a partir de dados de controle fornecidos como um dicionário JSON,
    utilizando um template HTML do Jinja2.
    """
    rows = []
    for control_id, control_info in processed_controls['Controls'].items():
        control_parts = control_info.split(';')
        control_name, rationale = control_parts[0], ';'.join(control_parts[1:]) if len(control_parts) > 1 else "N/A"

        # Constrói as chaves para buscar Audit, Remediation e Reference usando o sufixo do control_id
        suffix = control_id[7:]  # Assume que o prefixo 'Control' tem 7 caracteres e obtém o sufixo numérico
        audit = processed_controls['Audits'].get(f'Audit{suffix}', 'N/A')
        remediation = processed_controls['Remediations'].get(f'Remediation{suffix}', 'N/A')
        reference = processed_controls['References'].get(f'Reference{suffix}', 'N/A')

        rows.append({
            'ControlID': control_id,
            'Control': control_name,
            'Rationale': rationale,
            'Audit': audit,
            'Remediation': remediation,
            'Reference': reference
        })

    # Carrega o template e gera o HTML
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('template_baseline.html')
    html_output = template.render(rows=rows)

    # Salva o HTML no arquivo especificado
    with open(output_file_path, 'w') as file:
        file.write(html_output)

    print(f"HTML gerado com sucesso e salvo em '{output_file_path}'.")




async def create_baseline(technology, ticket):
    """Main function to create a baseline for a given technology."""
    assistant_manager = OpenAIAssistantManager(api_key)
    assistant_id = BASELINESECURITYEXPERT_ID
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
    print("##################################################################")
    print(processed_controls)
    print("##################################################################")

    save_data(processed_controls, ticket, technology)

    output_file_path = f'data/baselines/{ticket}_{technology}_{timestamp}.html'
    generate_html_from_processed_controls(processed_controls, TEMPLATE_DIR, output_file_path)