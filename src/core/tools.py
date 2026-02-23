from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper


def get_search_tool():
    """
    Returns a configured DuckDuckGo search tool.
    """
    wrapper = DuckDuckGoSearchAPIWrapper(region="cl-es", time="y", max_results=5)
    search = DuckDuckGoSearchRun(api_wrapper=wrapper, name="ddg_search_chile")
    return search
