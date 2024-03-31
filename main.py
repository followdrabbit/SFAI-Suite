import asyncio
import argparse
from dotenv import load_dotenv
from src.baseline_creator import create_baseline

async def main():
    # Configuração inicial
    load_dotenv()  # Carrega variáveis de ambiente do arquivo .env
    parser = argparse.ArgumentParser(description='Generate a security baseline for a new technology.')

    # Define os argumentos de linha de comando
    parser.add_argument('-tec', '--technology', type=str, required=True, help='The name of the new technology')

    # Analisa os argumentos fornecidos
    args = parser.parse_args()

    # Chama a função para criar a baseline, agora apenas com o argumento da tecnologia
    await create_baseline(technology=args.technology)

if __name__ == "__main__":
    asyncio.run(main())
