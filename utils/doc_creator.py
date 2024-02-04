import pandas as pd
import json
from jinja2 import Environment, FileSystemLoader

# Caminho para o arquivo JSON com os dados
json_file_path = '../data/structured/baseline/0001_Amazon S3_20240204_105410.json'


# Lendo o arquivo JSON
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Preparando os dados para o DataFrame
rows = []
for control_id, control_text in data['Controls'].items():
    control_info = control_text.split(". ")
    control = control_info[0].split("CONTROL: ")[1]
    rationale = control_info[1].split("RATIONALE: ")[1]
    audit = data['Audits'][control_id.replace('Control', 'Audit')]
    remediation = data['Remediations'][control_id.replace('Control', 'Remediation')]
    rows.append({
        'ControlID': control_id,
        'Control': control,
        'Rational': rationale,
        'Audit': audit,
        'Remediation': remediation
    })

# Convertendo para DataFrame
df = pd.DataFrame(rows)

# Configuração do Jinja2 para carregar o template do diretório 'templates'
env = Environment(loader=FileSystemLoader('../templates'))

# Carregando o template chamado 'template_baseline.html'
template = env.get_template('template_baseline.html')

# Renderizando o template com os dados do DataFrame
html_output = template.render(rows=df.to_dict(orient='records'))

# Salvando o HTML renderizado em um arquivo
output_file_path = 'output.html'
with open(output_file_path, 'w') as file:
    file.write(html_output)

print(f"HTML gerado com sucesso e salvo em '{output_file_path}'.")
