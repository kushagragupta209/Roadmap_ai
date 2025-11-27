import streamlit as st
import uuid
from groq_llama import model_call, model_call_question
import json

# ----------------------------------------------------
# MUST BE FIRST STREAMLIT COMMAND
# ----------------------------------------------------
st.set_page_config(page_title="Interactive Roadmap", layout="wide")


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
# MAIN PROCEED FUNCTION
# ----------------------------------------------------
def proceed(query_input, syllabus_input, data):

    # Sidebar navigation (NO NORMALIZATION)
    view_choice = st.sidebar.selectbox(
        "Go to:",
        ["Roadmap", "Topics", "Practice"],
        key="view_choice"
    )

    if view_choice == "Roadmap":

        st.subheader("🗺️ Interactive Roadmap")
        st.caption("Zoom with scroll • Drag to move • Reset anytime")

        mermaid_interactive(data["roadmap_mermaid"], height=700)

        st.success("Tip: Use touchpad gestures or your mouse wheel to zoom smoothly.")
    
    elif view_choice == "Practice":
        st.subheader("📘 Practice Questions")

        topic_names = [t["name"] for t in data["topics"]]

        selected_topic_name = st.selectbox(
            "Select Topic:",
            topic_names,
            key="practice_topic_choice"
        )

        selected_topic_1 = next(t for t in data["topics"] if t["name"] == selected_topic_name)

        subtopic_names_1 = [s["title"] for s in selected_topic_1["subtopics"]]

        selected_subtopic_title_1 = st.selectbox(
            "Select Subtopic:",
            subtopic_names_1,
            key="practice_subtopic_choice"
        )

        # 👉 ONLY BUTTON VISIBLE BEFORE CLICK
        if st.button("Generate Practice Questions"):
            st.session_state.practice_questions = model_call_question(
                selected_subtopic_title_1,
                selected_topic_name,
                "difficult"
            )
            st.session_state.practice_questions_clicked = True

        # 👉 SHOW QUESTIONS ONLY AFTER CLICK
        if st.session_state.get("practice_questions_clicked", False):

            questions_data = st.session_state.practice_questions

            if isinstance(questions_data, dict) and "questions" in questions_data:
                for i, q in enumerate(questions_data["questions"], start=1):
                    with st.expander(f"Question {i}"):
                        if isinstance(q, dict):
                            st.write(f"**{q.get('question', 'No question')}**")

                            if "options" in q:
                                st.write("**Options:**")
                                for opt in q["options"]:
                                    st.write(f"- {opt}")

                            if "answer" in q:
                                with st.expander("Answer"):
                                    st.success(q["answer"])

                            if "explanation" in q:
                                with st.expander("Explanation"):
                                    st.info(q["explanation"])

                        elif isinstance(q, str):
                            st.write(q)

            elif isinstance(questions_data, list):
                for i, q in enumerate(questions_data, start=1):
                    with st.expander(f"Question {i}"):
                        st.write(q)

            else:
                st.error("⚠️ Could not parse practice questions.")

    else:
        st.subheader("Explore Topics")

        topic_names = [t["name"] for t in data["topics"]]

        selected_topic_name = st.selectbox(
            "Topic:",
            topic_names,
            key="topic_choice"
        )

        selected_topic = next(t for t in data["topics"] if t["name"] == selected_topic_name)

        subtopic_names = [s["title"] for s in selected_topic["subtopics"]]

        selected_subtopic_title = st.selectbox(
            "Subtopic:",
            subtopic_names,
            key="subtopic_choice"
        )

        selected_subtopic = next(
            s for s in selected_topic["subtopics"]
            if s["title"] == selected_subtopic_title
        )

        with st.expander("Study Resources", expanded=True):
            for link in selected_subtopic["study_links"]:
                st.markdown(f"- [Open]({link})")

        with st.expander("Practice Problems"):
            for link in selected_subtopic["practice_links"]:
                st.markdown(f"- [Open]({link})")

        with st.expander("Previous Year Questions"):
            for link in selected_subtopic["previous_year_questions"]:
                st.markdown(f"- [Open]({link})")

    st.info("You can switch back to the roadmap from the left sidebar.")


@st.cache_resource
def load_data_once(query_input, syllabus_input):
    return model_call(query_input, syllabus_input)


query_input = st.sidebar.text_input("What exam are you preparing for?", key="query_input")
syllabus_input = st.sidebar.text_input("Add Syllabus/Topic/Subject?", key="subject_input")

if "proceed_clicked" not in st.session_state:
    st.session_state.proceed_clicked = False

if st.sidebar.button("Generate"):
    st.session_state.proceed_clicked = True
    st.session_state.data = load_data_once(query_input, syllabus_input)

if st.session_state.proceed_clicked:
    print("Data - ", st.session_state.data)
    proceed(query_input, syllabus_input, st.session_state.data)