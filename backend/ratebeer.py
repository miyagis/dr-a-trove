from langchain_community.tools.tavily_search import TavilySearchResults
from config import set_env_variables
from langchain.schema import Document

set_env_variables()
web_search_tool = TavilySearchResults(max_results=3)

def web_search(location):
    """
    Web search based on the re-phrased question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates documents key with appended web results
    """
    query = f"breweries in city {location} site:ratebeer.com"
    documents = []
    web_results = web_search_tool.invoke({"query": query})
    documents.extend(
        [
            Document(page_content=d["content"], metadata={"url": d["url"]})
            for d in web_results
        ]
    )

    return documents


def tool_ratebeer_get_breweries_by_location(location):
    """
    This function searches the web to resolve questions on recent topics that are unlikely to be found in books.
    """
    breweries = []
    get_web_sources = web_search(location)

    for url in get_web_sources:
        print (url)
    
    return breweries 


if __name__ == '__main__':
    tool_ratebeer_get_breweries_by_location('Aalst')