import pandas as pd
import os
from jinja2 import Template

# Substitua 'caminho_para_sua_planilha.xlsx' pelo caminho real da sua planilha
file_path = 'caminho_para_sua_planilha.xlsx'
sheet_name = 'Hardening'
required_columns = ['Control', 'Applicability', 'Rational', 'Audit', 'Remediation']
id_prefix = "CTRL-"

# Verifique se o arquivo existe
if not os.path.exists(file_path):
    print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
else:
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"Erro: As seguintes colunas estão faltando: {', '.join(missing_columns)}")
        else:
            df = df[required_columns]
            df.insert(0, 'ControlID', [f"{id_prefix}{str(i).zfill(3)}" for i in range(1, 1 + len(df))])

            # Carregar o template HTML de um arquivo externo
            with open('template_html.html', 'r') as file:
                template_html = file.read()

            template = Template(template_html)

            # Renderizar o template HTML com os dados do DataFrame
            html_output = template.render(rows=df.to_dict(orient='records'))

            # Salvar o HTML em um arquivo
            with open('output.html', 'w') as file:
                file.write(html_output)

            print("HTML gerado com sucesso e salvo em 'output.html'.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
