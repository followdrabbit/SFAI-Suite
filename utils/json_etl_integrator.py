import json
import asyncio

class JsonETLIntegrator:
    def __init__(self):
        pass

    async def read_json_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    async def extract_info(self, messages):
        for message in messages:
            if message['role'] == 'assistant':
                try:
                    # Encontrar o índice do primeiro e último caracteres de um objeto JSON válido
                    start_index = message['message'].find('```json') + 7  # +7 para pular '```json'
                    end_index = message['message'].find('```', start_index)
                    if start_index != -1 and end_index != -1:
                        json_str = message['message'][start_index:end_index].strip()
                        print(json_str)  # Passo de depuração
                        return json.loads(json_str)
                    else:
                        print("Objeto JSON não encontrado na mensagem.")
                        return None
                except json.JSONDecodeError as e:
                    print("Erro ao decodificar JSON:", e)
                    return None

        return None

async def main():
    file_path = '../data/raw/result_messages.json'
    integrator = JsonETLIntegrator()
    
    messages = await integrator.read_json_file(file_path)
    result = await integrator.extract_info(messages)
    print("Resultado:", result)

asyncio.run(main())
