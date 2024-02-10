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



async def get_controls(ticket, technology):
    thread_id = await thread_manager.create_thread()
    prompt_updated = replace_text_in_file(BASELINE_GET_CONTROLS_PROMPT, PRODUCT_NAME_PLACEHOLDER, technology)
    print(f"Getting controls for: {technology}")
    await thread_manager.create_message(thread_id, prompt_updated)
    run_id = await runs_manager.create_run(thread_id, BASELINESECURITYEXPERT_ID)
    await runs_manager.process_run(thread_id, run_id)
    print(f"Controls obtained for: {technology}!")
    return thread_id

async def check_controls(thread_id, ticket, technology):
    prompt_updated = replace_text_in_file(BASELINE_CHECK_CONTROLS, PRODUCT_NAME_PLACEHOLDER, technology)
    print("Reviewing controls")
    await thread_manager.create_message(thread_id, prompt_updated)
    run_id = await runs_manager.create_run(thread_id, SECURITYGUARDIANAI_ID)
    thread_data = await runs_manager.process_run(thread_id, run_id)
    print("Revised controls!")
    return thread_data

def save_data(data, ticket, technology, base_dir=DATA_DIR):
    try:
        file_path = os.path.join(base_dir, f"{ticket}_{technology}_{timestamp}.json")
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {file_path}")
    except Exception as e:
        print (e)

async def create_baseline(technology, ticket):
    thread_id = await get_controls(ticket, technology)
    thread_data = await check_controls(thread_id, ticket, technology)
    save_data(thread_data, ticket, technology, DATA_RAW_DIR)
