# Imports corrigidos conforme os nomes fornecidos originalmente
import json
import os
import re
import asyncio
import pandas as pd
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from utils.thread_manager import OpenAIThreadManager
from utils.assistant_manager import OpenAIAssistantManager
from utils.runs_manager import OpenAIRunsManager
from utils.text_replacer import replace_text_in_file
from utils.files_manager import OpenAIFilesManager


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Constantes
API_KEY = os.getenv("OPENAI_API_KEY")
BASELINESECURITYEXPERT_ID = os.getenv("BASELINESECURITYEXPERT_ID")
SECURITYGUARDIANAI_ID = os.getenv("SECURITYGUARDIANAI_ID")
PRODUCT_NAME_PLACEHOLDER = "PRODUCT_NAME"
CONTROL_NAME_PLACEHOLDER = "CONTROL_NAME"
DATA_RAW_DIR = "data/raw"
DATA_DIR = "data"
BASELINE_GET_CONTROLS_PROMPT = 'prompts/baseline_get_controls.txt'
BASELINE_CHECK_CONTROLS = 'prompts/baseline_check_controls.txt'
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
thread_manager = OpenAIThreadManager(API_KEY)
runs_manager = OpenAIRunsManager(API_KEY)
file_manager = OpenAIFilesManager(API_KEY)
assistant_manager = OpenAIAssistantManager(API_KEY)
thread_id = None  # Variável global declarada fora das funções
chat_data = None  # Variável global declarada fora das funções

async def create_and_process_run(thread_id, prompt_source, placeholder, technology, assistant_id):
    prompt_updated = replace_text_in_file(prompt_source, placeholder, technology)
    await thread_manager.create_message(thread_id, prompt_updated)
    run_id = await runs_manager.create_run(thread_id, assistant_id)
    data = await runs_manager.process_run(thread_id, run_id)
    return data

async def get_controls(technology):
    global thread_id
    thread_id = await thread_manager.create_thread()
    print("######################################################")
    print (f"            Getting controls for {technology}")
    print("######################################################")
    await create_and_process_run(thread_id, BASELINE_GET_CONTROLS_PROMPT, PRODUCT_NAME_PLACEHOLDER, technology, BASELINESECURITYEXPERT_ID)

async def check_controls(ticket, technology):
    global thread_id
    global chat_data
    print("######################################################")
    print ("                Reviewing controls")
    print("######################################################")
    chat_data = await create_and_process_run(thread_id, BASELINE_CHECK_CONTROLS, PRODUCT_NAME_PLACEHOLDER, technology, SECURITYGUARDIANAI_ID)

def save_data(data, ticket, technology, base_dir=DATA_DIR):
    try:
        file_path = os.path.join(base_dir, f"{ticket}_{technology}_{timestamp}.json")
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {file_path}")
    except Exception as e:
        print (e)

async def create_baseline(technology, ticket):
    await get_controls(technology)
    await check_controls(ticket, technology)
    save_data(chat_data, ticket, technology, DATA_RAW_DIR)
