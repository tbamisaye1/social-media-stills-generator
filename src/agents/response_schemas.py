from pydantic import BaseModel
from typing import Literal
# Structured response from langchain expects a Basemodel hence why we shoudlnt use the respone in state.py 
class Model_Response(BaseModel):
    verdict: Literal["keep", "discard"] | None #optional
    description: str