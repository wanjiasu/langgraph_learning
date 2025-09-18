from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class UserState(TypedDict):
    is_premium: bool
    message: str

def greet_user(state: UserState) -> UserState:
    state["message"] = "Hello!"
    return state

def premium_greeting(state: UserState) -> UserState:
    state["message"] += " Thank you for being a premium user!"
    return state

def regular_greeting(state: UserState) -> UserState:
    state["message"] += " Thank you for being a regular user!"
    return state

def check_subscription(state: UserState) -> str:
    if state["is_premium"]:
        return "premium_greeting"
    else:
        return "regular_greeting"

graph = StateGraph(UserState)
graph.add_node("greet_user", greet_user)
graph.add_node("premium_greeting", premium_greeting)
graph.add_node("regular_greeting", regular_greeting)
graph.add_node("check_subscription", check_subscription)

graph.add_edge(START, "greet_user")
graph.add_conditional_edges("greet_user", check_subscription)
graph.add_edge("premium_greeting", END)
graph.add_edge("regular_greeting", END)

graph = graph.compile()
result = graph.invoke({"is_premium": False, "message": ""})
print(result)