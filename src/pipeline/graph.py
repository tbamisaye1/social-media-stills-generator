"""Define the graph for our agent"""
from langgraph.graph import StateGraph, START, END
from pipeline.state import AgentState
# conditional nodes


# conditional node:
def conditional_node(state: AgentState) -> AgentState:
    # this is a ghost node, it doesn't do anything, it just returns the state
    return state



from agents.nodes import load_images, classify_image, get_next_image
graph = StateGraph(AgentState)
graph.add_node("load_images", load_images)
graph.add_node("classify_image", classify_image)
graph.add_node("get_next_image", get_next_image)
graph.add_node("conditional_node", conditional_node)


# Conditional edge router

def conditional_edge_router(state: AgentState) -> str:
    if state["current_image_index"] < len(state["images"]) and state["current_image"] is not None:
        return "classify_image"
    else:
        return "end"
# Define edeges
graph.add_edge(START, "load_images")
graph.add_edge("load_images", "conditional_node") #where our ReACT loop starts
graph.add_conditional_edges("conditional_node", conditional_edge_router, {
    "classify_image": "classify_image",
    "end": END,
})
graph.add_edge("classify_image", "get_next_image")
graph.add_edge("get_next_image", "conditional_node")


app = graph.compile()

final_State = app.invoke({"current_image_index": 0, "current_image": None, "images": [], "results": []})
print("================================================")
print(f"Final state: {final_State}", "\n")
print("================================================")