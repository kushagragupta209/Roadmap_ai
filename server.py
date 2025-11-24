from mcp.server import Server
from tools.google_search import google_search_tool
from tools.mermaid_tool import mermaid_tool

server = Server(
    tools=[
        google_search_tool,
        mermaid_tool
    ]
)

if __name__ == "__main__":
    server.run()