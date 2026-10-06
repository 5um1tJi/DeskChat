from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END, START
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from typing import TypedDict, Annotated, Literal
from langgraph.graph.message import add_messages
import operator
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv(override=True)

llm = ChatGroq(
    model="openai/gpt-oss-20b",
)

class chatStat(TypedDict):
    mess : Annotated[list[BaseMessage], add_messages]

def message(state: chatStat):
    mess = state["mess"]

    res = llm.invoke(mess)

    return {"mess" : [res]}



graph = StateGraph(chatStat)
check = InMemorySaver()
graph.add_node("message" , message)

graph.add_edge(START, "message")
graph.add_edge("message", END)

workflow = graph.compile(checkpointer=check)

# while True:
#     user_mess = input("Type here : ")
#     print(user_mess)

#     if user_mess.strip().lower() in ["quit", "bye", "end", "exit", "band Karo"]:
#         break

#     response = workflow.invoke({"mess" : [HumanMessage(content=user_mess)]})

#     print("AI answer - ", response["mess"][-1].content)