from src.core.tools import get_search_tool
import sys

try:
    tool = get_search_tool()
    print("Tool initialized.")
    query = "Hospital Dr. Antonio Tirado Lanas Ovalle oncologia"
    print(f"Running query: {query}")
    res = tool.invoke(query)
    print(f"Result Type: {type(res)}")
    print(f"Result Repr: {repr(res)}")
    print("--- Result Content ---")
    print(res)
    print("----------------------")
except Exception as e:
    print(f"Error: {e}")
    import traceback

    traceback.print_exc()
