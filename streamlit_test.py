import streamlit as st
import uuid
from groq_llama import model_call

# ----------------------------------------------------
# MUST BE FIRST STREAMLIT COMMAND
# ----------------------------------------------------
st.set_page_config(page_title="Interactive Roadmap", layout="wide")


# ----------------------------------------------------
# DATA
# ----------------------------------------------------
@st.cache_resource
def load_data_once():
    return model_call()

data = load_data_once() 
print(data)

# ----------------------------------------------------
# FUNCTION: INTERACTIVE MERMAID GRAPH (Zoom + Pan)
# ----------------------------------------------------

def mermaid_interactive(mermaid_code: str, height=650):

    element_id = f"m_{uuid.uuid4().hex}"

    html_code = f"""
    <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
        <button onclick="pz.reset();" 
                style="padding:4px 12px; border-radius:6px; border:1px solid #ccc; cursor:pointer;">
            🔄 Reset Zoom
        </button>
    </div>

    <div id="{element_id}" style="width: 100%; height: {height}px; 
         border: 2px solid #bbb; border-radius: 10px; overflow: hidden; background:#f8f9fa;"></div>

    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/panzoom@9.4.0/dist/panzoom.min.js"></script>

    <script>
        mermaid.initialize({{ startOnLoad: false }});
        const code = `{mermaid_code.replace('`', '')}`;

        mermaid.render("render_{element_id}", code).then(({{
            svg
        }}) => {{
            const container = document.getElementById("{element_id}");
            container.innerHTML = svg;

            const svgEl = container.querySelector("svg");

            svgEl.style.width = "100%";
            svgEl.style.height = "100%";

            // Enable pan & zoom
            pz = panzoom(svgEl, {{
                maxZoom: 5,
                minZoom: 0.5,
                zoomSpeed: 0.065
            }});
        }});
    </script>
    """

    st.components.v1.html(html_code, height=height + 50)


# ----------------------------------------------------
# SIDEBAR NAVIGATION (Dropdown)
# ----------------------------------------------------
st.sidebar.title("📂 Navigation")
view_choice = st.sidebar.selectbox(
    "Go to:",
    ["🗺️ Roadmap", "📚 Topics"]
)

# Normalize selection for logic
if "Roadmap" in view_choice:
    view_choice = "Roadmap"
else:
    view_choice = "Topics"


# ----------------------------------------------------
# MAIN TITLE
# ----------------------------------------------------
st.title("📘 Interactive Probability & Statistics Roadmap")
st.write("A modern, interactive learning dashboard.")


# ----------------------------------------------------
# VIEW: INTERACTIVE ROADMAP
# ----------------------------------------------------
if view_choice == "Roadmap":

    st.subheader("🗺️ Interactive Roadmap")
    st.caption("Zoom with scroll • Drag to move • Reset anytime")

    mermaid_interactive(data["roadmap_mermaid"], height=700)

    st.success("Tip: Use touchpad gestures or your mouse wheel to zoom smoothly.")


# ----------------------------------------------------
# VIEW: TOPIC DETAILS
# ----------------------------------------------------
else:
    st.subheader("📚 Explore Topics")

    # 1st dropdown → choose a topic
    topic_names = [t["name"] for t in data["topics"]]
    selected_topic_name = st.selectbox("Choose a Topic:", topic_names)

    # get topic dict
    selected_topic = next(t for t in data["topics"] if t["name"] == selected_topic_name)

    # 2nd dropdown → choose its subtopic
    subtopic_names = [s["title"] for s in selected_topic["subtopics"]]
    selected_subtopic_title = st.selectbox("Choose a Subtopic:", subtopic_names)

    # get subtopic dict
    selected_subtopic = next(
        s for s in selected_topic["subtopics"] 
        if s["title"] == selected_subtopic_title
    )

    # UI section
    st.markdown(f"## 📌 {selected_subtopic_title}")

    with st.expander("🎥 Study Resources", expanded=True):
        for link in selected_subtopic["study_links"]:
            st.markdown(f"- [Open]({link})")

    with st.expander("🧠 Practice Problems"):
        for link in selected_subtopic["practice_links"]:
            st.markdown(f"- [Open]({link})")

    with st.expander("📝 Previous Year Questions"):
        for link in selected_subtopic["previous_year_questions"]:
            st.markdown(f"- [Open]({link})")

    st.info("You can switch back to the roadmap from the left sidebar.")