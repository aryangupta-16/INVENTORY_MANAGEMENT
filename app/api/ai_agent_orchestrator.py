from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from agents import Runner, SQLiteSession  # @unresolvedImports
from app.utils.security import get_current_user
from app.agents.orchestrator_agent import orchestrator_agent
from app.repository.product_repository import list
from sqlalchemy.orm import Session # @unresolvedImports
from app.config.database import get_db
from dotenv import load_dotenv
load_dotenv()
import os

router = APIRouter(prefix="/ai", tags=["AI"])



class QueryRequest(BaseModel):
    query: str # optionally you can pass a list of SKUs to focus on

class QueryResponse(BaseModel):
    text: str
    # You can also return trace or structured output if you want

@router.post("/chat", response_model=QueryResponse)
async def chat(req: QueryRequest ,db: Session = Depends(get_db), user=Depends(get_current_user)):
    # Here we skip user management for simplicity; you should pass user context
    query = req.query
    
    # product_ids = list(db,user.id)
    # product_ids = req.product_ids or ["prod_1"]  # default list if none given

    # Create a session for this conversation (optional memory)
    # session = SQLiteSession("session1")  # you can use better session IDs

    # Run the orchestrator agent
    print(os.getenv("OPENAI_API_KEY"))
    
    prompt = f"query: {query}, user_id: {user.id}"
     
    result = await Runner.run(
        orchestrator_agent,
        prompt
        # session=session
    )

    return QueryResponse(text=result.final_output)
