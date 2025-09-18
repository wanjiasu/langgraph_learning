from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize the OpenAI client
model = ChatOpenAI(
    model="gpt-4o-mini", 
    api_key=os.getenv("YUNWU_API_KEY"),
    base_url=os.getenv("YUNWU_BASE_URL")
)

def cal_llm(state: MessagesState) -> MessagesState:
    messages = state["messages"]
    response = model.invoke(messages[-1].content)
    return {"messages": [response]}

# define the graph
workflow = StateGraph(MessagesState)
workflow.add_node("cal_llm", cal_llm)
workflow.add_edge(START, "cal_llm")
workflow.add_edge("cal_llm", END)

app = workflow.compile()



# 连续获取用户输入的函数
def interact_with_agent():
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            break

        input_messages = {
            "messages": [HumanMessage(content=user_input)]
        }

        # run the workflow
        for chunk in app.stream(input_messages, stream_mode="values"):
            chunk['messages'][-1].pretty_print()


if __name__ == "__main__":
    interact_with_agent()