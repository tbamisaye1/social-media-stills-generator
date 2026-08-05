"""Define the graph for our agent"""
from langgraph.graph import StateGraph, START, END
from pipeline.state import AgentState
import json
import os
import dotenv
dotenv.load_dotenv()
output_dir = os.getenv("OUTPUT_DIR")
import shutil



# conditional nodes


# conditional node:
def conditional_node(state: AgentState) -> AgentState:
    # this is a ghost node, it doesn't do anything, it just returns the state
    return state




from agents.nodes import load_images, classify_image, get_next_image, save_images
graph = StateGraph(AgentState)
graph.add_node("load_images", load_images)
graph.add_node("classify_image", classify_image)
graph.add_node("get_next_image", get_next_image)
graph.add_node("conditional_node", conditional_node)
graph.add_node("save_images", save_images)
# graph.add_node("conditional_empty_images", conditional_empty_images)
# Conditional edge router

def conditional_edge_router(state: AgentState) -> str:
    if state["current_image_index"] < len(state["images"]) and state["current_image"] is not None:
        return "classify_image"
    else:
        return "end"
    
    
    
def conditional_empty_images_router(state: AgentState) -> AgentState:
    input_dir = os.getenv("INPUT_DIR")
    images = os.listdir(input_dir)
    images = [image for image in images if  image.lower().endswith((".jpg", ".jpeg", ".png"))]
    
    if len(images) == 0:
        return "end"
    else:
        return "load_images"

# Define edeges
graph.add_conditional_edges(START, conditional_empty_images_router, {
    "end": END,
    "load_images": "load_images",
})
graph.add_edge("load_images", "conditional_node") #where our ReACT loop starts
graph.add_conditional_edges("conditional_node", conditional_edge_router, {
    "classify_image": "classify_image",
    "end": "save_images",
})
graph.add_edge("classify_image", "get_next_image")
graph.add_edge("get_next_image", "conditional_node")
graph.add_edge("save_images", END)

app = graph.compile()

final_State = app.invoke({"current_image_index": 0, "current_image": None, "images": [], "results": []})
# print("================================================")
# print(f"Final state: {final_State}", "\n")
# print("================================================")

# Process output into a file
output_file = os.path.join(output_dir, "results.json")
json_results = [{
    "image" : result["image"],
    "image_index" : result["image_index"],
    "verdict": result["result"].verdict,
    "description": result["result"].description
} for result in final_State["results"]]


successes = [{
    "image" : result["image"],
    "image_index" : result["image_index"],
    "verdict": result["result"].verdict,
    "description": result["result"].description
} for result in final_State["results"] if result["result"].verdict == "keep"]
    
    

with open(output_file, "w") as f:
    json.dump(json_results, f,indent=3)
    
