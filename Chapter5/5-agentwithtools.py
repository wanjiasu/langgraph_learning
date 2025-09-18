from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode

load_dotenv()



# define the tool
@tool
def get_weather(location: str) -> str:
    """Get the current weather for a given location.
    
    Args:
        location: The city name to get weather for
        
    Returns:
        A string describing the weather condition
    """
    weather_data = {
        "New York": "Sunny",
        "Los Angeles": "Cloudy",
        "Chicago": "Rainy",
        "Houston": "Sunny",
        "Miami": "Sunny",
        "Seattle": "Rainy",
        "San Francisco": "Sunny",
    }
    return weather_data.get(location, "Unknown")

tool_node = ToolNode(tools=[get_weather])

# Initialize the OpenAI client
model = ChatOpenAI(
    model="gpt-4o-mini", 
    api_key=os.getenv("YUNWU_API_KEY"),
    base_url=os.getenv("YUNWU_BASE_URL")
).bind_tools([get_weather])

def cal_llm(state: MessagesState) -> MessagesState:
    messages = state["messages"]
    response = model.invoke(messages[-1].content)

    if response.tool_calls:
        tool_result = tool_node.invoke({'messages': [response]})
        tool_message = tool_result['messages'][-1].content
        response.content = f"\nTool Result:{tool_message}"
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

        # run the workflow - LangSmith 会自动追踪
        for chunk in app.stream(input_messages, stream_mode="values"):
            chunk['messages'][-1].pretty_print()

if __name__ == "__main__":
    interact_with_agent()