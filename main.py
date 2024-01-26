import argparse
from src.controls.controls_creator import create_baseline_request
from utils.get_assistant_id import get_id

def main():
    try:
        parser = argparse.ArgumentParser(description='Calls controls_creator with technology and ticket parameters.')

        # Defines arguments for technology and ticket with short forms -t and -T
        parser.add_argument('-tec', '--technology', type=str, required=True, help='The new technology name')
        # Descomente e ajuste conforme necessário
        # parser.add_argument('-tic', '--ticket', type=str, required=True, help='The ticket associated with the change')

        # Parses the provided arguments
        args = parser.parse_args()

        # Calls the function get_id and gets the assistant id
        assistant_id = get_id()

        # Calls the controls_creator function with the technology and possibly ticket parameters
        # Ajuste conforme necessário para incluir o ticket
        create_baseline_request(technology=args.technology, assistant_id=assistant_id)

    except argparse.ArgumentError as arg_err:
        # Específico para erros de argumentos
        print(f"Error with arguments: {arg_err}")
    except Exception as e:
        # Captura exceções gerais
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
