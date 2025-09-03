from pydantic import BaseModel
from typing import List, Optional

class CompareRequest(BaseModel):
    prompt: str
    models: List[str]

class ModelResponse(BaseModel):
    model: str
    text: str
    latency_ms: int
    tokens: Optional[int] = None
    cost: Optional[float] = None

class CompareResponse(BaseModel):
    results: List[ModelResponse]
