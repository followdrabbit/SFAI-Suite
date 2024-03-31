
# SafeGuardAI

SafeGuardAI is a tool designed to assist in the implementation of robust security practices, using Artificial Intelligence to analyze and assess the security of systems. It offers an efficient way to create security baselines, automate vulnerability detection, and provide personalized security recommendations.

## Requirements to Use SafeGuardAI

- Install the Python libraries described in the `requirements.txt` file.
- Create an API key from [OpenAI](https://platform.openai.com/api-keys) and [Tavily](https://app.tavily.com/home).
- Have a balance in your OpenAI account, as queries are paid for as [detailed here](https://platform.openai.com/docs/guides/production-best-practices/managing-costs).

## Installation

To install the necessary dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Configuring SafeGuardAI

SafeGuardAI has a script called `setup.py` that configures the environment and gets it ready for use. Just run the script with the command below and provide the OpenAI and Tavily API keys as requested.

```bash
python setup.py
```

### Setup Configuration Process

1. Request the OpenAI and Tavily API keys.
2. Remove existing configurations: This includes removing the `.env` file, assistants, and files stored in the account.
3. Create the assistants.
4. Upload the files and link them with the "SecurityFileAnalyzer" and "AWSSecurityAuditor" assistants.
5. Store the provided API keys and IDs of the created assistants in a `.env` file.

## How Does SafeGuardAI Work?

1. Conducts a WEB search consisting of 2 stages:
   - Lists 10 websites with security recommendations related to the informed service/product.
   - Extracts the security configurations from each listed site.
2. Analyzes the files linked to the assistant and extracts recommendations related to the informed service/product.
3. Asks an assistant to list security recommendations for the service/product informed based on best practices from CIS, NIS, AWS, and STIG.
4. Performs an analysis comparing the files linked to the assistant and the recommendations provided by the previous assistants.
5. Unifies all the previous recommendations.
6. Saves the entire chat history in the "data/raw" directory.

## Examples of Use

To use SafeGuardAI, simply type "python main.py -tec 'PRODUCT_NAME'", for example: "python main.py -tec 'Amazon S3'".

## TO DO

- Remove file upload from setup.
- Allow file upload for each execution.
- Support vendors other than AWS and allow use for technologies that are not cloud-based, such as Operating Systems and others.
- Refactor the code according to best practices.
- Create baselines using HTML templates

## License

MIT as described in the LICENSE file.