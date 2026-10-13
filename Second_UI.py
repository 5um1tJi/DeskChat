import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage
from main import workflow

st.set_page_config(
    page_title="My Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
<style>
    /* Gradient Title */
    .chat-title {
        background: linear-gradient(90deg, #FF4B4B, #FF8C00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 0px;
    }
    
    /* Thread Badge Container for Sidebar */
    .thread-badge {
        background-color: #f0f2f6;
        border-left: 4px solid #FF4B4B;
        padding: 8px 14px;
        border-radius: 6px;
        font-weight: 600;
        color: #31333F;
        font-size: 0.95rem;
        margin-bottom: 15px;
    }
    @media (prefers-color-scheme: dark) {
        .thread-badge {
            background-color: #262730;
            color: #FAFAFA;
        }
    }
    
    /* Subtle Chat Bubble Padding */
    .stChatMessage {
        border-radius: 12px;
        padding: 8px 12px;
    }
</style>
""", unsafe_allow_html=True)

if "thread_name" not in st.session_state:
    st.session_state["thread_name"] = "General Chat"

if "selected_persona" not in st.session_state:
    st.session_state["selected_persona"] = "Expert"

if "mess" not in st.session_state:
    st.session_state["mess"] = [
        {"role": "assistant", "content": "Welcome to **Bhai ka Chatbot**! 😎 What are we working on today?"}
    ]
PERSONA_PROMPTS = {
    "Expert": "You are a highly skilled technical expert. Provide detailed, accurate, and structured answers.",
    "Desi Bhai": "You are 'Bhai ka Chatbot', a cool, encouraging AI friend speaking in a helpful, casual Indian-English 'Bhai' tone. Use emojis like 😎, 💪, 🚀.",
    "Code Mentor": "You are a senior software developer and mentor. Focus on clean code, best practices, step-by-step logic, and detailed explanations.",
    "Concise": "Give direct, highly concise, bulleted responses without filler text."
}
with st.sidebar:
    st.title("⚙️ Controls")
    st.markdown(
        f"<div class='thread-badge'>🧵 Active Thread:<br><b>{st.session_state['thread_name']}</b></div>", 
        unsafe_allow_html=True
    )
    new_thread_name = st.text_input(
        "🏷️ Name your Thread:",
        value=st.session_state["thread_name"],
        placeholder="e.g. DSA Practice, Project Ideas..."
    )
    if new_thread_name != st.session_state["thread_name"]:
        st.session_state["thread_name"] = new_thread_name
        st.rerun()

    st.markdown("---")
    if st.button("🗑️ Clear Chat History", type="primary", use_container_width=True):
        st.session_state["mess"] = [
            {"role": "assistant", "content": f"Welcome to **{st.session_state['thread_name']}**! 😎 How can I help you?"}
        ]
        st.rerun()
conversation_started = any(msg["role"] == "user" for msg in st.session_state["mess"])
if not conversation_started:
    st.markdown("<h1 class='chat-title'>🤖 MY Chatbot</h1>", unsafe_allow_html=True)
    st.markdown("")
    st.markdown("**Choose AI Mode:**")
    col1, col2, col3, col4 = st.columns(4)

    if col1.button("🧠 Act as Expert", use_container_width=True, type="primary" if st.session_state["selected_persona"] == "Expert" else "secondary"):
        st.session_state["selected_persona"] = "Expert"
        st.toast("Switched mode to: Expert 🧠")
        
    if col2.button("😎 General", use_container_width=True, type="primary" if st.session_state["selected_persona"] == "Desi Bhai" else "secondary"):
        st.session_state["selected_persona"] = "Desi Bhai"
        st.toast("Switched mode to: Desi Bhai 😎")

    if col3.button("💻 Code Mentor", use_container_width=True, type="primary" if st.session_state["selected_persona"] == "Code Mentor" else "secondary"):
        st.session_state["selected_persona"] = "Code Mentor"
        st.toast("Switched mode to: Code Mentor 💻")

    if col4.button("⚡ Concise", use_container_width=True, type="primary" if st.session_state["selected_persona"] == "Concise" else "secondary"):
        st.session_state["selected_persona"] = "Concise"
        st.toast("Switched mode to: Concise ⚡")

    st.markdown("---")
for message in st.session_state["mess"]:
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state["mess"].append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    confi = {
        "configurable": {
            "thread_id": st.session_state["thread_name"]
        }
    }
    active_prompt = PERSONA_PROMPTS[st.session_state["selected_persona"]]
    messages_payload = [
        SystemMessage(content=active_prompt),
        HumanMessage(content=user_input)
    ]
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking... 🧠"):
            try:
                response = workflow.invoke({"mess": messages_payload}, config=confi)
                ai_message = response["mess"][-1].content
            except Exception as e:
                ai_message = f"❌ **Error running workflow:** `{str(e)}`"

            st.markdown(ai_message)
    st.session_state["mess"].append({"role": "assistant", "content": ai_message})
    st.rerun()