from langchain.tools import DuckDuckGoSearchResults, WikipediaQueryRun
from langchain.document_loaders import WebBaseLoader

from langchain.utilities import WikipediaAPIWrapper
    
def wikipedia_search_tool(input):
    wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    return wiki.run(input)

def duckduckgo_search_tool(input):
    ddg = DuckDuckGoSearchResults()
    return ddg.run(input)

def website_scraping_tool(input):
    loader = WebBaseLoader(input)
    return loader.load()