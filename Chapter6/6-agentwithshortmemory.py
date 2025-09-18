from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

# Initialize the OpenAI client
model = ChatOpenAI(
    model="gpt-4o-mini", 
    api_key=os.getenv("YUNWU_API_KEY"),
    base_url=os.getenv("YUNWU_BASE_URL")
)

def cal_llm(state: MessagesState) -> MessagesState:
    messages = state["messages"]
    # 传递所有历史消息给模型，而不是只传递最后一条
    response = model.invoke(messages)
    # 返回所有消息（包括历史消息和新响应）
    return {"messages": messages + [response]}

# define the graph
workflow = StateGraph(MessagesState)
workflow.add_node("cal_llm", cal_llm)
workflow.add_edge(START, "cal_llm")
workflow.add_edge("cal_llm", END)

checkpoint = MemorySaver()
app = workflow.compile(checkpointer=checkpoint)

# 连续获取用户输入的函数
def interact_with_agent():
    thread_id = "1"
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            break
        input_message = {
            "messages": [HumanMessage(content=user_input)],
        }
        config = {"configurable": {"thread_id": thread_id}}
        for chunk in app.stream(input_message, config=config, stream_mode="values"):
            chunk['messages'][-1].pretty_print()

if __name__ == "__main__":
    interact_with_agent()