import os
import requests
from mcp.server import Tool
from dotenv import load_dotenv

load_dotenv("env/.env")

SERPER_API_KEY = os.getenv("serper_api_key")
SERPER_URL = "https://google.serper.dev/search"

google_search_tool = Tool(
    name="google_search",
    description="Performs a Google Search using Serper API.",
)

@google_search_tool.run
def run_google_search(q: str, num: int = 5):
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {"q": q, "num": num}

    response = requests.post(SERPER_URL, json=payload, headers=headers)

    if response.status_code != 200:
        return {
            "error": f"Search failed: {response.status_code}",
            "details": response.text
        }

    data = response.json()

    results = []
    if "organic" in data:
        for item in data["organic"][:num]:
            results.append({
                "title": item.get("title"),
                "snippet": item.get("snippet"),
                "link": item.get("link")
            })

    return {
        "query": q,
        "count": len(results),
        "results": results
    }