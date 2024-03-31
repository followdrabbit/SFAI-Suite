from tavily import TavilyClient
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente
load_dotenv()

# Constantes
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

class TavilyOperations:
    def __init__(self):
        self.client = TavilyClient(TAVILY_API_KEY)

    def tavily_get_search_context(self, query):
        response  = self.client.get_search_context(query, search_depth="advanced", max_results=10, include_raw_content=True, max_tokens=80000)
        return response

    def tavily_search(self, query):
        response  = self.client.search(query, search_depth="advanced")
        context = [{"url": obj["url"], "content": obj["content"]} for obj in response.results]
        return context

    def tavily_search_content(self, query):
        response  = self.client.get_search_context(query, search_depth="advanced", max_results=10, include_raw_content=True, max_tokens=80000)
        context = [{"url": obj["url"], "content": obj["content"]} for obj in response.results]
        return context