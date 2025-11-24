import base64
import streamlit as st
from io import BytesIO
from PIL import Image
import uuid

def mermaid_to_png(mermaid_code: str):
    """
    Convert mermaid diagram to PNG using Mermaid.js in Streamlit.
    Renders SVG in browser → sends SVG back → convert to PNG in Python.
    """

    # Unique ID so multiple diagrams don't conflict
    element_id = f"mermaid_{uuid.uuid4().hex}"

    # HTML + JS for rendering Mermaid and sending back the SVG
    mermaid_renderer = f"""
        <div id="{element_id}"></div>
        <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
        <script>
            const code = `{mermaid_code.replace('`','')}`;

            mermaid.initialize({{ startOnLoad: false }});
            mermaid.render("rendered_{element_id}", code)
            .then(({{
                svg
            }}) => {{
                const div = document.getElementById("{element_id}");
                div.innerHTML = svg;

                // Send SVG back to Streamlit Python
                const svgBase64 = btoa(svg);
                window.parent.postMessage({{
                    type: "mermaid_svg",
                    id: "{element_id}",
                    data: svgBase64
                }}, "*");
            }});
        </script>
    """

    # Streamlit displays the HTML renderer
    st.components.v1.html(mermaid_renderer, height=400)

    # Wait for browser to send back SVG
    svg_msg = st.session_state.get(f"svg_{element_id}")

    if svg_msg:
        svg_data = base64.b64decode(svg_msg)
        img = Image.open(BytesIO(svg_data))
        png_io = BytesIO()
        img.save(png_io, format="PNG")
        png_io.seek(0)
        return png_io  # Return PNG file-like object

    return None