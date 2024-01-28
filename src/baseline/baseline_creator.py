import asyncio
from utils.run import run_thread
from utils.get_result import check_assistant_status
from utils.thread_manager import OpenAIThreadManager
from utils.text_replacer import replace_text_in_file
from utils.asssistant_manager import OpenAIAssistantManager


async def create_baseline(technology, api_key):

    # Create an instance of the assistant manager with the API key
    assistant_manager = OpenAIAssistantManager(api_key)

    # Call the list_assistants method and get the unique assistants
    unique_assistants = await assistant_manager.list_assistants()

    # Find the ID of the assistant named "Cloud Security Expert"
    assistant_id = None
    for name, id in unique_assistants.items():
        if name == "Cloud Security Expert":
            assistant_id = id
            break

    if assistant_id is None:
        print("Assistant 'Cloud Security Expert' not found.")
        return

    # Create an instance of the assistant manager with the API key
    thread_manager = OpenAIThreadManager(api_key)

    # Criando uma nova thread
    new_thread_id = await thread_manager.create_thread()
    print("ID da nova thread criada:", new_thread_id)

    # Calls the function resposible for update the prompt with the provided technology
    new_prompt = replace_text_in_file('prompts/controls_prompt.txt', 'PRODUCT_NAME', technology)

    # Criando uma nova mensagem na thread criada
    new_message = await thread_manager.create_message(new_thread_id, new_prompt)
    print("Detalhes da nova mensagem:", new_message)

    # Calls the run_thread function and gets the 
    run_id=run_thread(new_thread_id, assistant_id)


    # Calls the get_result function
    check_assistant_status(new_thread_id, run_id, assistant_id)