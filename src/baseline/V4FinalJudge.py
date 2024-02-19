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
from tavily import TavilyClient

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Constantes
API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
BASELINESECURITYEXPERT_ID = os.getenv("BASELINESECURITYEXPERT_ID")
SECURITYGUARDIANAI_ID = os.getenv("SECURITYGUARDIANAI_ID")
EXTERNALRESEARCHER_ID = os.getenv("EXTERNALRESEARCHER_ID")
DOCWRITER_ID = os.getenv("DOCWRITER_ID")
DATA_RAW_DIR = "data/raw"
DATA_DIR = "data"
PROMPT1 = 'prompts/FinalJudgePart1'
PROMPT2 = 'prompts/FinalJudgePart2'
PROMPT3 = 'prompts/FinalJudgePart3'
PROMPT4 = 'prompts/FinalJudgePart4'
PROMPT5 = 'prompts/FinalJudgePart5'
PROMPT6 = 'prompts/FinalJudgePart6'
TECHNOLOGY_PLACEHOLDER = 'PRODUCT_NAME'
WEBPAGE_PLACEHOLDER = 'WEBPAGE_PLACEHOLDER'
FILENAME_PLACEHOLDER = 'FILENAME_PLACEHOLDER'
CONTENT_PLACEHOLDER = 'CONTENT_PLACEHOLDER'
GET_CONTROLS_PROMPT = 'prompts/AIControlsManagerBaselineBuilderInitiate.txt'
CHECK_CONTROLS_PROMPT = 'prompts/AIControlsManagerBaselineIntegratorAnalyze.txt'
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
thread_manager = OpenAIThreadManager(API_KEY)
runs_manager = OpenAIRunsManager(API_KEY)
file_manager = OpenAIFilesManager(API_KEY)
assistant_manager = OpenAIAssistantManager(API_KEY)
tavily_client = TavilyClient(TAVILY_API_KEY)
thread_id = None  # Variável global declarada fora das funções
chat_data = None  # Variável global declarada fora das funções


def message_display(message):
    total_width = 60
    fill_char = '#'
    centered_message = message.center(total_width, fill_char)
    print("")
    print(centered_message)
    print("")

async def create_message_and_run(thread_id, prompt, assistant_id):
    await thread_manager.create_message(thread_id, prompt)
    run_id = await runs_manager.create_run(thread_id, assistant_id)
    print(f"----> New run created with ID: {run_id}")
    return run_id

async def process_run(thread_id, run_id):
    print("----> Checking run status...")
    data = await runs_manager.process_run(thread_id, run_id)
    return data

async def create_new_tread():
    global thread_id
    thread_id = await thread_manager.create_thread()
    message_display("  Creating Thread  ")
    print(f"----> New thread created with ID: {thread_id}")

# Function to perform a Tavily search
def tavily_search(query):
    search_result = tavily_client.get_search_context(query, search_depth="advanced", max_tokens=30000)
    return search_result

# Function to handle tool output submission
async def submit_tool_outputs(thread_id, run_id, tools_to_call):
    tool_output_array = []
    for tool in tools_to_call:
        output = None
        tool_call_id = tool.id
        function_name = tool.function.name
        function_args = tool.function.arguments

        if function_name == "tavily_search":
            output = tavily_search(query=json.loads(function_args)["query"])

        if output:
            tool_output_array.append({"tool_call_id": tool_call_id, "output": output})

    print("----> Sending required information...")
    await runs_manager.submit_tool_outputs(thread_id, run_id, tool_output_array)

async def tavily_preambule(prompt):
    run_id = await create_message_and_run(thread_id, prompt, EXTERNALRESEARCHER_ID)
    run_data = await process_run(thread_id, run_id)
    try:
        tools_to_call = run_data.required_action.submit_tool_outputs.tool_calls
        await submit_tool_outputs(thread_id, run_id, tools_to_call)
        data = await process_run(thread_id, run_id)
        return data
    except Exception as e:
        pass

async def get_controls_from_web(technology):
    prompt = replace_text_in_file(PROMPT1, TECHNOLOGY_PLACEHOLDER, technology)
    message_display("  Starting search in the WEB  ")
    raw_data = await tavily_preambule(prompt)
    extracted_data = extract_response(raw_data)
    page_count = 1
    for control in extracted_data.split('\n\n'):
        print(f"----> Getting recommendations for page {page_count}...")
        prompt = replace_text_in_file(PROMPT2, WEBPAGE_PLACEHOLDER, control)
        prompt = prompt.replace(TECHNOLOGY_PLACEHOLDER, technology)
        await tavily_preambule(prompt)
        page_count += 1

async def get_controls_from_file(technology):
    FILENAME = 'Trend Micro S3 - AWS S3 Best Practices'
    extract_prompt = replace_text_in_file(PROMPT3, TECHNOLOGY_PLACEHOLDER, technology)
    extract_prompt = extract_prompt.replace(FILENAME_PLACEHOLDER, FILENAME)
    message_display("  Starting search in the file  ")
    run_id = await create_message_and_run(thread_id, extract_prompt, SECURITYGUARDIANAI_ID)
    await process_run(thread_id, run_id)
    review_prompt = replace_text_in_file(PROMPT4, FILENAME_PLACEHOLDER, FILENAME)
    message_display("  Starting Review  ")
    run_id = await create_message_and_run(thread_id, review_prompt, SECURITYGUARDIANAI_ID)
    await process_run(thread_id, run_id)

async def get_controls_from_ai(technology):
    ai_controls_prompt = replace_text_in_file(PROMPT5, TECHNOLOGY_PLACEHOLDER, technology)  
    message_display("  Getting recommendations from AI  ")
    run_id = await create_message_and_run(thread_id, ai_controls_prompt, BASELINESECURITYEXPERT_ID)
    await process_run(thread_id, run_id)

async def generate_baseline(technology):
    global chat_data
    generate_baseline_prompt = replace_text_in_file(PROMPT6, TECHNOLOGY_PLACEHOLDER, technology)  
    message_display("  Generating document  ")
    run_id = await create_message_and_run(thread_id, generate_baseline_prompt, DOCWRITER_ID)
    chat_data = await process_run(thread_id, run_id)

def extract_response(raw_data):
    """Extracts assistant messages from the raw response."""
    messages = []
    for item in (item for sublist in raw_data for item in (sublist if isinstance(sublist, list) else [sublist])):
        if item.get('role') == 'assistant':
            messages.append(item.get('message', ''))
    extracted_data = " ".join(messages)
    return extracted_data
    
def save_data(data, ticket, technology, base_dir=DATA_DIR):
    try:
        file_path = os.path.join(base_dir, f"V4FinalJudge{ticket}_{technology}_{timestamp}.json")
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {file_path}")
    except Exception as e:
        print (e)

async def create_baseline(technology, ticket):
    await create_new_tread()
    await get_controls_from_web(technology)
    await get_controls_from_file(technology)
    await get_controls_from_ai(technology)
    await generate_baseline(technology)
    save_data(chat_data, ticket, technology, DATA_RAW_DIR)


'''
TO DO
- [ ] Gerar baseline usando o template
- [ ] Gerar Relatório com considerações adicionais
'''