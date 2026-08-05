"""This module contains all of the node functions which we will use to build our main agentic graph"""

from pipeline.state import AgentState
from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv
import os
from agents.response_schemas import Model_Response
from prompts.ai_prompts import VISION_SYSTEM_PROMPT, VISION_USER_PROMPT
from agents.response_schemas import Model_Response
from pipeline.state import ImageResult
load_dotenv()
from tools.image_tools import image_path_to_base64
import shutil
from dotenv import load_dotenv
load_dotenv()
output_dir = os.getenv("OUTPUT_DIR")

def load_images(state: AgentState) -> AgentState:
    """Load the images from the input directory"""
    input_dir = os.getenv("INPUT_DIR")
    images = os.listdir(input_dir)
    images = [image for image in images if  image.lower().endswith((".jpg", ".jpeg", ".png"))]
    images = [os.path.join(input_dir, image) for image in images]
    return {"images": images, "current_image_index": 0, "current_image": images[0]}


# def filter_images(state: AgentState) -> AgentState:
#     """Filter the images based on the criteria"""
#     for image in state["images"]:
        
        
def classify_image(state: AgentState) -> AgentState:
    """Classify the image based on the criteria by getting a judgement from our vision llm"""
    image = state["current_image"]
    converted_image = image_path_to_base64(image)
    vision_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    structured_vision_llm = vision_llm.with_structured_output(Model_Response)
    result = structured_vision_llm.invoke([SystemMessage(VISION_SYSTEM_PROMPT),
                    HumanMessage(content=[ {"type": "text", "text": VISION_USER_PROMPT},
                    {"type": "image_url", "image_url": {"url": converted_image}} ])
                    ])
    formatted_ai_result = Model_Response(verdict=result.verdict, description=result.description)
    state["results"].append(ImageResult(image=image, result=formatted_ai_result, image_index=state["current_image_index"]))
    # To be built out later
    # !!! Error: .append()returns None so we can thave .append() on state update
    return state


def get_next_image(state: AgentState) -> AgentState:
    """Get the next image from the list of images"""
    if state["current_image_index"] <= len(state["images"]) - 1: #neds to increment on the last one for the cindiotnla router to fail
        state["current_image_index"] += 1
        if state["current_image_index"] >= len(state["images"]):
            return state
        state["current_image"] = state["images"][state["current_image_index"]]
    return state



def save_images(state: AgentState) -> AgentState:
    """Save the images classified as keep to the output directory"""
    for result in state["results"]:
        if result["result"].verdict == "keep":
            shutil.copy(result["image"], output_dir)
    return state