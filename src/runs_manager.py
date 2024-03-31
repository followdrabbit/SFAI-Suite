# Import necessary libraries
import openai
import asyncio
import os
import json
from dotenv import load_dotenv  # Used for loading environment variables

# Define a class to manage interactions with OpenAI's API
class OpenAIRunsManager:
    def __init__(self, api_key):
        # Initialize the manager with an OpenAI API key
        self.client = openai.AsyncClient(api_key=api_key)

    # Asynchronously create a new run
    async def create_run(self, thread_id: str, assistant_id: str):
        run = await self.client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)
        return run.id

    # Asynchronously retrieve information about a specific run
    async def retrieve_run(self, thread_id: str, run_id: str):
        return await self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

    def update_run(self, thread_id, run_id, metadata=None, extra_headers=None, extra_query=None, extra_body=None, timeout=None):
            """
            Modifies a run.

            Args:
                thread_id: The ID of the thread the run belongs to.
                run_id: The ID of the run to update.
                metadata: Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format. Keys can be a maximum of 64 characters long and values can be a maxium of 512 characters long.
                extra_headers: Send extra headers
                extra_query: Add additional query parameters to the request
                extra_body: Add additional JSON properties to the request
                timeout: Override the client-level default timeout for this request, in seconds
            """
            return self.client.threads.runs.update(
                    thread_id=thread_id,
                    run_id=run_id,
                    metadata=metadata,
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout
            )

    # Asynchronously list all runs associated with a thread
    async def list_runs(self, thread_id, limit=20, order="desc", after=None, before=None, extra_headers=None, extra_query=None, extra_body=None, timeout=None):
            """
            Returns a list of runs belonging to a thread.

            Args:
                thread_id: The ID of the thread to list runs from.
                limit: A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.
                order: Sort order by the `created_at` timestamp of the objects. `asc` for ascending order and `desc` for descending order.
                after: A cursor for use in pagination. `after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include after=obj_foo in order to fetch the next page of the list.
                before: A cursor for use in pagination. `before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include before=obj_foo in order to fetch the previous page of the list.
                extra_headers: Send extra headers
                extra_query: Add additional query parameters to the request
                extra_body: Add additional JSON properties to the request
                timeout: Override the client-level default timeout for this request, in seconds
            """
            return await self.client.beta.threads.runs.list(
                    thread_id=thread_id, 
                    limit=limit, 
                    order=order, 
                    after=after, 
                    before=before,
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout
            )

    # Asynchronously cancel a specific run
    async def cancel_run(self, thread_id, run_id, extra_headers=None, extra_query=None, extra_body=None, timeout=None):
            """
            Cancels a run.

            Args:
                thread_id: The ID of the thread the run belongs to.
                run_id: The ID of the run to cancel.
                extra_headers: Send extra headers
                extra_query: Add additional query parameters to the request
                extra_body: Add additional JSON properties to the request
                timeout: Override the client-level default timeout for this request, in seconds
            """
            return await self.client.beta.threads.runs.cancel(
                    thread_id=thread_id,
                    run_id=run_id,
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout
            )



    # Asynchronously process a run and check its status
    async def process_run(self, thread_id: str, run_id: str):
        try:  
            while True:
                run = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
                
                if run.status == "queued":
                    print(f"Run status.............. {run.status}")
                    await asyncio.sleep(5)  # Wait for 5 seconds before checking the status again

                elif run.status == "in_progress":
                    print(f"Run status.............. {run.status}")
                    await asyncio.sleep(5)  # Wait for 5 seconds before checking the status again

                elif run.status == "completed":
                    print(f"Run status.............. {run.status}")
                    messages = openai.beta.threads.messages.list(thread_id=thread_id)

                    result_messages = []
                    for message in messages:
                        assert message.content[0].type == "text"
                        msg = {"role": message.role, "message": message.content[0].text.value}
                        result_messages.append(msg)
                    return result_messages

                elif run.status == "requires_action":
                    print(f"Run status.............. {run.status}")
                    return run

                elif run.status == "failed":
                    print("The run failed.")
                    print(f"Error: {json.dumps(str(run), indent=4)}")
                    exit(1)
                
                elif run.status == "expired":
                    print("The run expired.")
                    print(f"Error: {json.dumps(str(run), indent=4)}")
                    exit(1)

                else:
                    print(f"Unexpected run status:.....{run.status}")
                    print(f"Error: {json.dumps(str(run), indent=4)}")
                    exit(1)

        except Exception as e:
            print(f"Error checking the run status: {e}")


    async def submit_tool_outputs(self, thread_id: str, run_id: str, tool_outputs: list):
        try:
            return openai.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run_id,
                tool_outputs=tool_outputs
            )
        except Exception as e:
            print(f"Error: {e}")

# Main async function to execute the manager
async def main():
    load_dotenv()  # Load environment variables (like API keys)
    api_key = os.getenv("OPENAI_API_KEY")  # Get the OpenAI API key from environment variables
    run_manager = OpenAIRunsManager(api_key)  # Create an instance of the manager

    # Example usage (commented out)
    # run_id = await run_manager.create_run('your_thread_id', 'your_assistant_id')
    # result_messages = await run_manager.process_run('your_thread_id', run_id, 'your_ticket')
    # print(result_messages)

    # Suponha que você já tenha um thread_id e run_id válidos
    #thread_id = "seu_thread_id"
    #run_id = "seu_run_id"
    
    # Utilizando a função retrieve_run
    #run_info = await run_manager.retrieve_run(thread_id, run_id)
    #print(run_info)


    # thread_id = "thread_gaMOfhbZOySAlkyPXQP63AzH"
    # run_id = "run_vqptyJ3gmUebcQI8xYjWgqXY"
    # await run_manager.cancel_run(thread_id, run_id)
    

# Entry point of the script
if __name__ == "__main__":
    asyncio.run(main())  # Execute the main function asynchronously
