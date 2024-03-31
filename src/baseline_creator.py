import asyncio
import json
import os
from src.utils import message_display, save_data, replace_text_in_file, extract_response
from src.tavily_operations import TavilyOperations
from src.thread_manager import OpenAIThreadManager
from src.files_manager import OpenAIFilesManager
from src.assistant_manager import OpenAIAssistantManager
from src.runs_manager import OpenAIRunsManager
from dotenv import load_dotenv


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Constantes
API_KEY = os.getenv("OPENAI_API_KEY")
AWSSECURITYRESEARCHER_ID = os.getenv("AWSSECURITYRESEARCHER_ID")
SECURITYFILEANALYZER_ID = os.getenv("SECURITYFILEANALYZER_ID")
AWSSECURITYEXPERT_ID = os.getenv("AWSSECURITYEXPERT_ID")
AWSSECURITYAUDITOR_ID = os.getenv("AWSSECURITYAUDITOR_ID")
BASELINEWRITER_ID = os.getenv("BASELINEWRITER_ID")
PROMPT1 = "prompts/prompt1_list_webpages"
PROMPT2 = "prompts/prompt2_get_webpages_recommendations"
PROMPT3 = "prompts/prompt3_get_file_recommendations"
PROMPT4 = "prompts/prompt4_get_ai_recommendations"
PROMPT5 = "prompts/prompt5_audit_controls"
PROMPT6 = "prompts/prompt6_create_baseline"
chat_data = None

class BaselineCreator:
    def __init__(self, technology):
        self.technology = technology
        self.thread_manager = OpenAIThreadManager(API_KEY)
        self.file_manager = OpenAIFilesManager(API_KEY)
        self.assistant_manager = OpenAIAssistantManager(API_KEY)
        self.runs_manager = OpenAIRunsManager(API_KEY)
        self.tavily_operations = TavilyOperations()

    async def create_baseline(self):
        # Inicia um novo thread
        thread_id = await self.thread_manager.create_thread()
        message_display(f"New thread created with ID: {thread_id}")

        # Executa as etapas necessárias para coletar controles de segurança
        await self.collect_security_controls(thread_id)


    async def web_search(self, thread_id, prompt, assistant_id):
        try:
            await self.thread_manager.create_message(thread_id, prompt)
            run_id = await self.runs_manager.create_run(thread_id, assistant_id)
            print(f"----> New run created with ID: {run_id}")
            run_data = await self.runs_manager.process_run(thread_id, run_id)
            if run_data.status == "requires_action":
                tools_to_call = run_data.required_action.submit_tool_outputs.tool_calls
                tool_output_array = []
                for tool in tools_to_call:
                    output = None
                    tool_call_id = tool.id
                    function_name = tool.function.name
                    function_args = tool.function.arguments

                    if function_name == "tavily_search":
                        output = self.tavily_operations.tavily_search_content(query=json.loads(function_args)["query"])

                    if output:
                        tool_output_array.append({"tool_call_id": tool_call_id, "output": output})

                print("----> Sending required information...")
                await self.runs_manager.submit_tool_outputs(thread_id, run_id, tool_output_array)
                raw_data = await self.runs_manager.process_run(thread_id, run_id)
                return raw_data
        except Exception as e:
            print(f"Error: {e}")

    async def get_controls_from_web(self, thread_id):
        try:
            message_display("  Starting search in the WEB  ")
            updated_prompt = replace_text_in_file(PROMPT1, "PRODUCT_NAME", self.technology)
            raw_data = await self.web_search(thread_id, updated_prompt, AWSSECURITYRESEARCHER_ID)
            extracted_data = extract_response(raw_data)
            page_count = 1
            for control in extracted_data.split('\n\n'):
                print(f"----> Getting recommendations for page {page_count}...")
                updated_prompt = replace_text_in_file(PROMPT2, "WEBPAGE_PLACEHOLDER", control)
                updated_prompt = updated_prompt.replace("PRODUCT_NAME", self.technology)
                await self.web_search(thread_id, updated_prompt, AWSSECURITYRESEARCHER_ID)
                page_count += 1
        except Exception as e:
            print(f"Error: {e}")

    async def get_controls_from_file(self, thread_id):
        try:
            print()
        except Exception as e:
            print(f"Error: {e}")

    async def get_controls_from_files(self, thread_id):
        updated_prompt = replace_text_in_file(PROMPT3, "PRODUCT_NAME", self.technology)
        message_display("  Starting search in the file  ")
        await self.thread_manager.create_message(thread_id, updated_prompt)
        run_id = await self.runs_manager.create_run(thread_id, SECURITYFILEANALYZER_ID)
        print(f"----> New run created with ID: {run_id}")
        await self.runs_manager.process_run(thread_id, run_id)

    async def get_controls_from_ai(self, thread_id):
        updated_prompt = replace_text_in_file(PROMPT4, "PRODUCT_NAME", self.technology)  
        message_display("  Getting recommendations from AI  ")
        await self.thread_manager.create_message(thread_id, updated_prompt)
        run_id = await self.runs_manager.create_run(thread_id, AWSSECURITYEXPERT_ID)
        print(f"----> New run created with ID: {run_id}")
        await self.runs_manager.process_run(thread_id, run_id)

    async def audit_controls(self, thread_id):
        updated_prompt = replace_text_in_file(PROMPT5, "PRODUCT_NAME", self.technology)  
        message_display("  Auditing recommendations  ")
        await self.thread_manager.create_message(thread_id, updated_prompt)
        run_id = await self.runs_manager.create_run(thread_id, AWSSECURITYAUDITOR_ID)
        print(f"----> New run created with ID: {run_id}")
        await self.runs_manager.process_run(thread_id, run_id)

    async def unify_controls(self, thread_id):
        global chat_data
        updated_prompt = replace_text_in_file(PROMPT6, "PRODUCT_NAME", self.technology)
        message_display("  Unifying recommendations  ")
        await self.thread_manager.create_message(thread_id, updated_prompt)
        run_id = await self.runs_manager.create_run(thread_id, BASELINEWRITER_ID)
        print(f"----> New run created with ID: {run_id}")
        chat_data = await self.runs_manager.process_run(thread_id, run_id)


    async def collect_security_controls(self, thread_id):
        try:
            await self.get_controls_from_web(thread_id)
            await self.get_controls_from_files(thread_id)
            await self.get_controls_from_ai(thread_id)
            await self.audit_controls(thread_id)
            await self.unify_controls(thread_id)
            save_data(chat_data, self.technology, "data\raw")

        except Exception as e:
            print(f"Error: {e}")


# Função helper para facilitar a chamada da classe BaselineCreator
async def create_baseline(technology):
    creator = BaselineCreator(technology)
    await creator.create_baseline()