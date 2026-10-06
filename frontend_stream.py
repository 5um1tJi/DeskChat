import streamlit as st
from main import workflow
from langchain_core.messages import HumanMessage
confi = {'configurable': {'thread_id': 'thread-1'}}

if 'mess' not in st.session_state:
    st.session_state['mess'] = []


for chat in st.session_state['mess']:
    with st.chat_message(chat['role']):
        st.text(chat['content'])


my_in = st.chat_input('Type here')

if my_in:
    st.session_state['mess'].append({'role': 'user', 'content': my_in})
    with st.chat_message('user'):
        st.text(my_in)

    
    resp = workflow.invoke({'mess': [HumanMessage(content=my_in)]}, config=confi)

    ai_wala = resp['mess'][-1].content

    st.session_state['mess'].append({'role': 'assistant', 'content': ai_wala})

    with st.chat_message('assistant'):
        st.text(ai_wala)