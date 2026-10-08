import streamlit as st
from langchain_core.messages import HumanMessage
from main import workflow


st.set_page_config(
    page_title="Mera Chatbot", page_icon="🤖", layout="centered"
)

st.title(" Mera ChatBot")
st.markdown("---")

confi = {"configurable": {"thread_id": "thread-1"}}
if "mess" not in st.session_state:
  st.session_state["mess"] = []

with st.sidebar:
  st.header("Settings")
  if st.button("Clear Chat History", type="primary"):
    st.session_state["mess"] = []
    st.rerun()

for message in st.session_state["mess"]:
  avatar = "👤" if message["role"] == "user" else "🤖"

  with st.chat_message(message["role"], avatar=avatar):
    st.markdown(message["content"])

mera = st.chat_input("Type your message here...")

if mera:
  st.session_state["mess"].append({"role": "user", "content": mera})

  with st.chat_message("user", avatar="👤"):
    st.markdown(mera)

  with st.chat_message("assistant", avatar="🤖"):
    with st.spinner("Thinking..."):
      resp = workflow.invoke(
          {"mess": [HumanMessage(content=mera)]}, config=confi
      )
      ai_message = resp["mess"][-1].content
      st.markdown(ai_message)
       
  st.session_state["mess"].append({"role": "assistant", "content": ai_message})