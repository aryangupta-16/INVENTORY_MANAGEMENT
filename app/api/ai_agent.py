# app/api/ai_agent.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # @unresolvedImports
from app.schema.AiSchema import AIRequest, AIResponse
from app.service import ai_service
from app.config.database import get_db  # your SQLAlchemy session dependency
from app.utils.security import get_current_user

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/chat", response_model=AIResponse)
def chat_ai(request: AIRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user_id = current_user.id
    response = ai_service.handle_ai_query(user_id, request.query)
    return response
