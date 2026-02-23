from duckduckgo_search import DDGS
import json

def test_search():
    query = "Normativa oncología Servicio Salud Coquimbo Hospital de Ovalle leyes unidades responsables"
    print(f"Testing query: {query}")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, region='cl-es', timelimit='y', max_results=5))
            print(f"Found {len(results)} results")
            print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_search()
