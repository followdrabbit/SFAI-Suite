from openai import AsyncClient
from dotenv import load_dotenv
import os
import asyncio


class OpenAIFilesManager:
    def __init__(self, api_key: str):
        """
        Initialize the manager with an asynchronous OpenAI client.
        The client is used for interacting with the OpenAI API.
        
        :param api_key: API key for authenticating with the OpenAI API.
        """
        self.client = AsyncClient(api_key=api_key)
    
    async def upload_file(self, file_path: str, file_purpose='assistants') -> dict:
        """
        Uploads a file to the OpenAI API for processing with a purpose of 'assistants'.
        
        :param file_path: Path to the file to be uploaded.
        :return: The response from the OpenAI API after file upload.
        """
        with open(file_path, "rb") as file:
            response = await self.client.files.create(
                file=file,
                purpose=file_purpose  # Purpose set to 'assistants' as required
            )
        return response

    async def list_files(self) -> list:
        """
        Lists all files uploaded to the OpenAI API.
        
        :return: A list of files.
        """
        files = await self.client.files.list()
        return files.data

    async def delete_file(self, file_id: str) -> dict:
        """
        Deletes a file from the OpenAI API.
        
        :param file_id: ID of the file to be deleted.
        :return: The response from the OpenAI API after file deletion.
        """
        response = await self.client.files.delete(file_id=file_id)
        return response


async def run_examples():
    # Load environment variables (API key) from the .env file
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    SECURITYGUARDIANAI = os.getenv("SECURITYGUARDIANAI_ID")

    file_manager = OpenAIFilesManager(api_key)

    # Exemplo de upload de arquivo
    #file_path = "../data/LKB/trendmicro-best-practice-s3.md"  # Substitua pelo caminho do arquivo a ser enviado
    #upload_response = await file_manager.upload_file(file_path)
    #print("Upload Response:", upload_response)

    # Exemplo de listagem de arquivos
    all_files = await file_manager.list_files()
    
    # Extrair apenas os IDs dos arquivos usando a notação de ponto para acessar o atributo 'id'
    #file_ids = [file.id for file in all_files]
    #print("File IDs:", file_ids)

    # Exemplo de deleção de arquivo
    # Para este exemplo, assumimos que você já tem um file_id.
    # Você pode obter um file_id do upload_response ou list_response.
    #file_id = "your_file_id_here"  # Substitua pelo ID do arquivo a ser deletado
    #delete_response = await file_manager.delete_file(file_id)
    #print("Delete Response:", delete_response)

if __name__ == "__main__":
    asyncio.run(run_examples())
