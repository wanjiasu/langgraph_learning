from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
import os
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode

load_dotenv()

# Initialize the OpenAI client
model = ChatOpenAI(
    model="gpt-4o-mini", 
    api_key=os.getenv("YUNWU_API_KEY"),
    base_url=os.getenv("YUNWU_BASE_URL")
)


# define the tool
@tool
def get_user_profile(user_id: str):
    """Get the user profile for a given user ID."""
    user_data = {
        "101": {"name": "John Doe", "age": 30, "email": "john.doe@example.com"},
        "104": {"name": "Jane Smith", "age": 25, "email": "jane.smith@example.com"}
    }
    return user_data.get(user_id, "User not Found !")
tools = [get_user_profile]
tool_node = ToolNode(tools=tools)

message_with_tool_call = AIMessage(
    content="",
    tool_calls=[{
        "name": "get_user_profile",
        "args": {"user_id": "101"},
        "id": "tool_call_id",
        "type": "tool_call"
    }]
)




    
    