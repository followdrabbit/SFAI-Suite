# Documentação do Baseline de Segurança para Amazon S3

Este documento descreve a estrutura do JSON utilizado para definir um baseline de segurança para recursos armazenados no Amazon S3. O JSON é composto por uma lista de controles de segurança, cada um detalhando práticas recomendadas para garantir a segurança dos dados armazenados no S3.

## Estrutura do JSON

O JSON é estruturado como um objeto contendo uma única chave `ControlesDeSegurancaAmazonS3`, que mapeia para uma lista de controles de segurança. Cada controle de segurança é um objeto que descreve uma prática de segurança específica.

### Campos de Cada Controle de Segurança

Cada controle de segurança inclui os seguintes campos:

- `DominioDeSeguranca`: Descreve a área de segurança à qual o controle está relacionado (por exemplo, "Gerenciamento de Identidade e Acesso", "Criptografia").
- `TipoDeControle`: Indica se o controle é um controle de acesso, controle técnico, etc.
- `Controle`: O nome do controle de segurança (por exemplo, "Políticas de Bucket", "Criptografia em Trânsito e em Repouso").
- `Descricao`: Uma descrição detalhada do controle, explicando o que ele faz e por que é importante para a segurança do Amazon S3.
- `DependeDeDefinicoesDaEmpresa`: Indica se a implementação do controle depende das políticas e definições específicas da empresa (`Sim`) ou se é uma prática padrão que pode ser aplicada universalmente (`Não`).

### Exemplo de Controle de Segurança

```json
{
  "DominioDeSeguranca": "Gerenciamento de Identidade e Acesso",
  "TipoDeControle": "Controle de Acesso",
  "Controle": "Políticas de Bucket",
  "Descricao": "Definir políticas de bucket restritivas seguindo o princípio do menor privilégio, permitindo acesso apenas às entidades necessárias.",
  "DependeDeDefinicoesDaEmpresa": "Sim"
}
