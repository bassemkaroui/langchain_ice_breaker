from langchain_community.tools.tavily_search import TavilySearchResults


def get_profile_url_tavily(query: str):
    """
    Searches a query from various trusted sources by Tavily (eg: Linkedin, Twitter)
    """

    search = TavilySearchResults()
    result = search.run(f"{query}")
    return result
