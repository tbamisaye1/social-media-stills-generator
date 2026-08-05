from langchain_core.tools import tool
from pathlib import Path
import base64
import os
from dotenv import load_dotenv
load_dotenv()

input_dir = os.getenv("INPUT_DIR")

"""All the tools for our agents"""


def image_path_to_base64(image_path: str) -> str:
    # full_path = Path(input_dir) / image_path
    raw_image = Path(image_path).read_bytes()
    base64_image_encoded = base64.b64encode(raw_image).decode("utf-8")
    # base64_image_url = f"data:image/jpeg;base64,{base64   _image_encoded}"
    suffix = Path(image_path).suffix.lower()
    file_type = "image/jpeg" if suffix in {".jpg", ".jpeg"} else "image/png"

    return f"data:{file_type};base64,{base64_image_encoded}"
