# app/models/ai_models.py
from pydantic import BaseModel
from typing import List, Optional

class AIRequest(BaseModel):
    query: str
    

class AIResponse(BaseModel):
    answer: str
    related_entries: Optional[List[dict]] = []
