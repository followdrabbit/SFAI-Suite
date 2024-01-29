import os

class EtlManager:
    def __init__(self):
        self.file_content = []

    def file_exists(self, file_path):
        """
        Verifica se o arquivo existe no caminho especificado.
        """
        return os.path.exists(file_path)

    def remove_empty(self, file_path):
        """
        Lê cada linha não vazia do arquivo e armazena na lista file_content.
        """
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    if line.strip():
                        self.file_content.append(line.strip())
        except FileNotFoundError:
            print("Arquivo não encontrado.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    def write_file(self, file_path):
        """
        Sobrescreve o arquivo com o conteúdo atualizado (sem linhas em branco).
        """
        try:
            with open(file_path, 'w') as file:
                for line in self.file_content:
                    file.write(line + '\n')
        except Exception as e:
            print(f"Ocorreu um erro ao escrever o arquivo: {e}")

    def print_file_content(self):
        """
        Imprime o conteúdo do arquivo que foi lido.
        """
        for line in self.file_content:
            print(line)

# Entry point
if __name__ == "__main__":
    manager = EtlManager()

    # Especificar o caminho do arquivo
    file_path = ("../data/structured/sample_0001_controls_20240128_210823_structured.txt")

    # Verificar se o arquivo existe
    if manager.file_exists(file_path):
        # Remove linhas em branco do arquivo e armazena o conteúdo atualizado
        manager.remove_empty(file_path)

        # Sobrescrever o arquivo original com o conteúdo atualizado
        manager.write_file(file_path)

        # Opcional: imprimir o conteúdo atualizado
        manager.print_file_content()
    else:
        print("O arquivo especificado não existe.")
