import openai
import asyncio
import os
import json
from typing import Optional
from dotenv import load_dotenv
import threading

class OpenAIThreadManager:
    def __init__(self, api_key):
        self.client = openai.AsyncClient(api_key=api_key)

    async def create_thread(self, messages: Optional[list] = None, metadata: Optional[dict] = None):
        thread = await self.client.beta.threads.create()
        print(f"New thread created with ID: {thread.id}")
        return thread.id

    async def retrieve_thread(self, thread_id: str):
        return await self.client.beta.threads.retrieve(thread_id) 

    async def update_thread(self, thread_id: str, metadata: dict):
        return await self.client.beta.threads.update(thread_id, metadata=metadata)

    async def delete_thread(self, thread_id: str):
        return await self.client.beta.threads.delete(thread_id)

    async def create_message(self, thread_id: str, content: str, role: str = "user"):
        return await self.client.beta.threads.messages.create(thread_id=thread_id, role=role, content=content)

    async def retrieve_message(self, thread_id: str, message_id: str):
        return await self.client.beta.threads.messages.retrieve(thread_id=thread_id, message_id=message_id)

    async def list_messages(self, thread_id: str, order: str = 'desc', after: Optional[str] = None,
                            before: Optional[str] = None):
        try:
            return await self.client.beta.threads.messages.list(thread_id=thread_id,
                                                                order=order,
                                                                after=after,
                                                                before=before
                                                                )
        except Exception as e:
            print(f"An error occurred while retrieving messages: {e}")
            return None

async def main():
    # Carregar a API key do ambiente ou de um arquivo .env
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    # Criar uma instância do gerenciador de threads
    thread_manager = OpenAIThreadManager(api_key)

    # Exemplo de operação - criar uma nova thread
    #new_thread_id = await thread_manager.create_thread()
    #print("ID da nova thread:", new_thread_id)

    # Exemplo de operação - deletar uma thread específica
    #thread_id = "id_da_thread_aqui"  # Substitua com o ID real da thread que você deseja excluir
    #delete_response = await thread_manager.delete_thread(thread_id)
    #print("Resposta da deleção:", delete_response)

    # Exemplo de operação - recuperar uma thread específica
    #thread_id = "id_da_thread_aqui"  # Substitua pelo ID real da thread que você deseja recuperar
    #thread_details = await thread_manager.retrieve_thread(thread_id)
    #print("Detalhes da thread recuperada:", thread_details)

    # Exemplo de operação - atualizar uma thread existente
    #thread_id = "id_da_thread_aqui"  # Substitua pelo ID real da thread que você deseja atualizar
    #new_metadata = {"chave": "valor"}  # Substitua com os novos metadados que você deseja definir
    #update_response = await thread_manager.update_thread(thread_id, new_metadata)
    #print("Resposta da atualização:", update_response)

    # Exemplo de operação - recuperar uma mensagem específica de uma thread
    #thread_id = "id_da_thread_aqui"  # Substitua pelo ID real da thread
    #message_id = "id_da_mensagem_aqui"  # Substitua pelo ID real da mensagem
    #message_details = await thread_manager.retrieve_message(thread_id, message_id)
    #print("Detalhes da mensagem recuperada:", message_details)

    # Exemplo de operação - listar mensagens de uma thread específica
    #thread_id = "id_da_thread_aqui"  # Substitua pelo ID real da thread
    #messages = await thread_manager.list_messages(thread_id)
    #print("Mensagens da thread:", messages)

    # Exemplo de operação - criar uma nova mensagem em uma thread específica
    #thread_id = "thread_NNt59EvjRSWuTeJkGBSg4jRX"  # Substitua pelo ID real da thread
    #content = "Test"  # Substitua pelo conteúdo da mensagem
    #message = await thread_manager.create_message(thread_id, content)
    #print("Mensagem criada:", message)

if __name__ == "__main__":
    asyncio.run(main())
