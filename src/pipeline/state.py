"""Use this module ffor defining our agent state dataclass"""
from typing import TypedDict, Literal
from agents.response_schemas import Model_Response

class ImageResult(TypedDict):
    image: str
    image_index: int = 0
    result: Model_Response

class AgentState(TypedDict):
    """The state for our agent regarding the image filtering process"""
    verdict: Literal["keep", "discard"] | None
    images: list[str] | None
    current_image: str | None
    current_image_index: int | None
    results: list[ImageResult] | None
    
