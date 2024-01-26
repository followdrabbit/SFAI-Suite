from utils.thread_creator import create_thread
from utils.run import run_thread
from utils.get_result import check_assistant_status


def create_baseline_request(technology, assistant_id):
    # Calls the create_thread function and gets the thread_id
    thread_id=create_thread('prompts/controls_prompt.txt', 'PRODUCT_NAME', technology)

    # Calls the run_thread function and gets the 
    run_id=run_thread(thread_id, assistant_id)


    # Calls the get_result function
    check_assistant_status(thread_id, run_id, assistant_id)