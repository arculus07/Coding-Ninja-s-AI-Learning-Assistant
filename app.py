import streamlit as st
from src.core.orchestrator import TutorOrchestrator
import textwrap

# --- Page Configuration ---
st.set_page_config(page_title="Coding Ninja's AI Learning Assistant",
                   page_icon="🥷",
                   layout="wide")

# --- Custom CSS and JavaScript for UI Enhancement ---
st.markdown("""
    <style>
        /* Import modern fonts */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

        /* Root variables for Coding Ninjas color scheme */
        :root {
            --primary-orange:#FF6200;
            --secondary-orange:#F28C38;
            --bg-white:#FFFFFF;
            --card-bg:#F5F5F5;
            --text-color:#333333;
            --button-bg:#000000;
            --button-text:#FFFFFF;
            --gradient-orange:linear-gradient(135deg,#FF6200,#F28C38);
        }

        /* General app styling */
        body,.stApp{font-family:'Poppins',sans-serif;background:var(--bg-white);color:var(--text-color);}

        /* Title styling */
        h1{
            background:var(--gradient-orange);
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;
            font-weight:700;
            text-align:left;
            animation:fadeIn 1s ease-in;
            display:inline-block;
        }

        /* Simplified link styling */
        a{color:var(--primary-orange);text-decoration:none;}
        a:hover{text-decoration:underline;}

        h2,h3{color:var(--primary-orange);}

        .stChatMessage{
            background:var(--card-bg);
            border-radius:10px;
            padding:15px;
            margin:10px 0;
            box-shadow:0 2px 6px rgba(0,0,0,0.1);
            animation:slideIn .5s ease-out;
        }

        .stButton>button{
            background:var(--button-bg);
            color:var(--button-text);
            border:1px solid #FFFFFF;
            border-radius:8px;
            padding:10px 20px;
            font-weight:600;
            transition:transform .3s ease,background .3s ease,color .3s ease;
        }
        .stButton>button:hover{
            background:#FFFFFF;color:#000000;transform:translateY(-2px);
            box-shadow:0 4px 12px rgba(0,0,0,0.2);
        }
        .stButton>button[kind="primary"]{background:#000000;color:#FFFFFF;}
        .stButton>button[kind="primary"]:hover{background:#FFFFFF;color:#000000;}

        /* Sidebar Styling */
        [data-testid="stSidebar"]{background:var(--card-bg);border-right:1px solid #ddd;}
        .stSidebar h2,.stSidebar h3{color:var(--primary-orange);}
        .stSidebar .stImage{border-radius:10px;box-shadow:0 2px 6px rgba(0,0,0,0.1);}

        #roadmap-container{
            background:var(--card-bg);
            border-radius:10px;
            padding:20px;
            box-shadow:0 2px 6px rgba(0,0,0,0.1);
            animation:bounceIn .8s ease;
            width:100%;
            margin:20px 0;
            position:relative;
            height:200px;
        }
        .roadmap-block{
            background:#FFFFFF;
            border:2px dashed #333333;
            border-radius:8px;
            padding:15px;
            text-align:center;
            width:150px;             /* Wider block */
            height:100px;            /* Taller block */
            display:flex;
            justify-content:center;
            align-items:center;
            position:absolute;
            font-weight:600;
            font-size:14px;
            color:#333333;
            box-shadow:0 2px 4px rgba(0,0,0,0.1);

            /* NEW — keep text on one line */
            white-space:nowrap;      /* prevent internal wrap */
            overflow:hidden;         /* hide overflow */
            text-overflow:ellipsis;  /* add … if still too long */
        }
        .roadmap-arrow{position:absolute;pointer-events:none;width:40px;height:40px;}

        .stForm{background:var(--card-bg);border-radius:10px;padding:15px;box-shadow:0 2px 6px rgba(0,0,0,0.1);}
        .stRadio>label{
            color:var(--text-color);
            background:rgba(255,98,0,0.05);
            padding:10px;border-radius:8px;margin:5px 0;
            transition:background .3s ease;
        }
        .stRadio>label:hover{background:rgba(255,98,0,0.1);}

        @keyframes fadeIn{from{opacity:0;}to{opacity:1;}}
        @keyframes slideIn{from{transform:translateX(-20px);opacity:0;}to{transform:translateX(0);opacity:1;}}
        @keyframes bounceIn{
            0%{transform:scale(0.95);opacity:0;}
            50%{transform:scale(1.05);}
            100%{transform:scale(1);opacity:1;}
        }
    </style>
""", unsafe_allow_html=True)

# --- Helper Functions ---
def display_roadmap(roadmap):
    """Displays the roadmap as a fixed horizontal block layout."""
    steps = roadmap[:4] if isinstance(roadmap, list) and roadmap else ["Step 1", "Step 2", "Step 3", "Step 4"]
    while len(steps) < 4:
        steps.append(f"Step {len(steps) + 1}")

    positions = [50, 240, 430, 620]
    arrow_positions = [200, 390, 580]

    html = '<div id="roadmap-container">'
    for i, step in enumerate(steps):
        html += f'<div class="roadmap-block" style="left:{positions[i]}px;top:40px;">{step}</div>'

    for pos in arrow_positions:
        html += f"""
        <svg class="roadmap-arrow" style="left:{pos}px;top:75px;">
            <path d="M0 15 L25 15 L20 10 M25 15 L20 20" stroke="#333" stroke-width="2" fill="none" />
        </svg>
        """
    html += '</div>'

    with st.container():
        st.markdown("### Your Personalized RoadMap")
        st.components.v1.html(html, height=220)

def process_step(step):
    step_type = step.get("type")
    step_data = step.get("data", {})
    if step_type == "roadmap":
        st.session_state.messages.append({"role": "assistant", "type": "roadmap", "content": step_data})
    elif step_type == "content":
        st.session_state.messages.append({"role": "assistant",
                                          "content": f"### {step_data.get('topic','')}\n\n{step_data.get('explanation','')}"})
        st.session_state.ui_state = 'in_lesson'
    elif step_type == "quiz":
        st.session_state.current_question = step_data
        st.session_state.ui_state = 'awaiting_answer'
    elif step_type == "final_summary":
        st.session_state.messages.append({"role": "assistant", "content": step_data.get('summary','')})
        st.session_state.summary_data = step_data
        st.session_state.ui_state = 'session_over'
    elif step_type == "error":
        st.error(step_data)
        st.session_state.ui_state = 'awaiting_topic'

def handle_proceed():
    try:
        step = next(st.session_state.learning_flow)
        process_step(step)
    except StopIteration:
        st.session_state.ui_state = 'session_over'

def handle_quiz_submission():
    user_answer = st.session_state.quiz_answer.split(":")[0]
    try:
        feedback_step = st.session_state.learning_flow.send(user_answer)
        feedback_data = feedback_step.get('data', {})
        is_correct = feedback_data.get('correct', False)
        feedback_text = feedback_data.get('feedback', 'Sorry, something went wrong.')
        color = "green" if is_correct else "red"
        st.session_state.messages.append(
            {"role": "assistant", "content": f":{color}[{feedback_text}]"})
        st.session_state.ui_state = 'in_lesson'
    except StopIteration:
        st.session_state.ui_state = 'session_over'

def handle_end_session():
    st.session_state.ui_state = 'awaiting_topic'
    st.session_state.messages = []
    st.rerun()

# --- Sidebar "About" Section ---
with st.sidebar:
    st.image("https://placehold.co/400x150/ffffff/FF6200?text=Coding+Ninjas", use_container_width=True)
    st.header("About this Project")
    st.markdown("This is an adaptive AI Tutor built for a **Coding Ninjas** assignment. "
                "It uses a multi-agent system with LangChain to create a personalized learning journey.")
    st.subheader("Developed By")
    st.markdown("**Ayush Ranjan**")
    st.markdown("ranjanayush918@gmail.com")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/ayushxranjan/) | "
                "[GitHub](https://github.com/arculus07) | "
                "[Twitter](https://x.com/ArcuLus_) | "
                "[Resume](https://drive.google.com/file/d/1UR8FToXbGTu2ffDWVNozmkJAqtKD1XWg/view?usp=sharing)")
    st.subheader("Important Acknowledgement")
    st.info("The Streamlit UI for this project was created with the assistance of Google's Gemini. "
            "The entire multi-agent backend logic, agent design, and system architecture were designed and implemented by Ayush Ranjan.")

# --- Session State Initialization ---
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = TutorOrchestrator()
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'learning_flow' not in st.session_state:
    st.session_state.learning_flow = None
if 'ui_state' not in st.session_state:
    st.session_state.ui_state = 'awaiting_topic'
if 'summary_data' not in st.session_state:
    st.session_state.summary_data = {}
if 'current_question' not in st.session_state:
    st.session_state.current_question = {}

# --- Main App ---
st.title("🥷 Coding Ninja's AI Learning Assistant")
st.caption("An Agentic Learning Tool by "
           "[Ayush Ranjan](https://www.linkedin.com/in/ayushxranjan/)")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("type") == "roadmap":
            display_roadmap(message["content"])
        else:
            st.markdown(message["content"])

# --- UI State Machine ---
if st.session_state.ui_state == 'awaiting_topic':
    if user_input := st.chat_input("Enter a valid Topic | Question. eg. Tell me about LLMs | Teach me GoLANG | What is StringTheory"):
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.learning_flow = st.session_state.orchestrator.run(user_input)
        st.session_state.ui_state = 'in_lesson'
        st.rerun()
else:
    controls = st.container()
    col1, col2, col3 = controls.columns([2, 2, 1])
    col3.button("⏹️ End Session", on_click=handle_end_session, use_container_width=True)

    if st.session_state.ui_state == 'awaiting_answer':
        q_data = st.session_state.current_question.get('question_item', {})
        progress = st.session_state.current_question.get('progress', '')
        with st.form("quiz_form"):
            st.markdown(f"**{progress}**: {q_data.get('question', 'N/A')}")
            options_dict = q_data.get('options', {})
            st.radio("Choose your answer:",
                     [f"{k}: {v}" for k, v in options_dict.items()],
                     key="quiz_answer", label_visibility="collapsed")
            st.form_submit_button("Submit Answer", on_click=handle_quiz_submission)

    elif st.session_state.ui_state == 'in_lesson':
        col1.button("▶️ Proceed", on_click=handle_proceed,
                    use_container_width=True, type="primary")

    elif st.session_state.ui_state == 'session_over':
        summary_data = st.session_state.summary_data
        if summary_data.get('offer_retest'):
            if col1.button("🔁 Take Re-Test", use_container_width=True):
                st.session_state.learning_flow = st.session_state.orchestrator.run_retest()
                st.session_state.ui_state = 'in_lesson'
                st.rerun()
        if col2.button("🚀 Start New Topic", use_container_width=True, type="primary"):
            handle_end_session()
