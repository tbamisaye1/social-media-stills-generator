from langchain_core.tools import tool
from pathlib import Path
import base64
import os
from dotenv import load_dotenv
import json
from langchain_core.messages import HumanMessage, AIMessage
from prompts.ai_prompts import VISION_USER_PROMPT
load_dotenv()

input_dir = os.getenv("INPUT_DIR")
Few_shot_folder = Path("data/calibration/few_shot/")
FEW_SHOT_LABELS = Few_shot_folder / "labels.json"
FEW_SHOT_IMAGES = Few_shot_folder / "images"



"""All the tools for our agents"""


def image_path_to_base64(image_path: str) -> str:
    # full_path = Path(input_dir) / image_path
    raw_image = Path(image_path).read_bytes()
    base64_image_encoded = base64.b64encode(raw_image).decode("utf-8")
    # base64_image_url = f"data:image/jpeg;base64,{base64   _image_encoded}"
    suffix = Path(image_path).suffix.lower()
    file_type = "image/jpeg" if suffix in {".jpg", ".jpeg"} else "image/png"

    return f"data:{file_type};base64,{base64_image_encoded}"


def _setup_load_examples_messages() -> list:
    labels = json.loads(FEW_SHOT_LABELS.read_text())
    messages = []
    for example in labels:
        data_url = image_path_to_base64(str(FEW_SHOT_IMAGES / example["file"]))
        messages.append(HumanMessage(content=[
            {"type": "text", "text": VISION_USER_PROMPT },
            {"type": "image_url", "image_url": {"url": data_url}}]
            ))
        # now we teeach the mdoel whte expected answer by giving it the description of the example
        messages.append(
            AIMessage(content=json.dumps({
                "verdict": example["verdict"],
                "description": example["description"],
            }))
        )
    
    return messages
# we will pass this into context as history wehn the graph starts the 
