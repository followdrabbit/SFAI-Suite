import openai
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a API Key do ambiente
api_key = os.getenv('OPENAI_API_KEY')

# Cria o cliente da OpenAI usando a API Key
client = openai.OpenAI(api_key=api_key)

assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview",
)
