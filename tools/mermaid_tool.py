from mcp.server import Tool

mermaid_tool = Tool(
    name="mermaid_diagram",
    description="Generate Mermaid flowchart syntax.",
)

@mermaid_tool.run
def run_mermaid_diagram(description: str):
    """
    This tool converts a plain English flow description into a Mermaid flowchart.
    The LLM will produce final diagram based on tool output.
    """

    return {
        "diagram": f"""
flowchart TD
    A[Start] --> B[{description}]
    B --> C[End]
"""
    }