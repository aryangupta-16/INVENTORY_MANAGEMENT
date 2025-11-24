# app/api/routes/chat.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.utils.security import get_current_user
from app.graph.graph_builder import build_graph, AgenticState

router = APIRouter()

# Build graph once on startup
workflow = build_graph()

@router.post("/chat/v1")
def agentic_chat(request: dict, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Unified entrypoint for all agentic queries.
    """
    user_query = request.get("query", "")

    # ✅ Initialize LangGraph state
    state = AgenticState(
        user_input=user_query,
        user_id=current_user.id,
        logs=[]
    )

    # ✅ Run the graph workflow
    final_state = workflow.invoke(state)

    # ✅ Return the response
    return {
        "response": final_state.get("agent_response"),
        "logs": final_state.get("logs")
    }
