from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.User_route import router as User
from app.api.Product_route import router as Product
from app.api.Stock_route import router as Stock
from app.api.Customer_route import router as Customer
from app.api.ai_agent import router as Ai
from app.api.ai_agent_orchestrator import router as AiAgent
from app.config.database import engine, Base
from app.utils.error_handler import init_exception_handlers
from dotenv import load_dotenv
load_dotenv()
import os 

print(os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# Base.metadata.drop_all(bind=engine) # @UndefinedVariable
Base.metadata.create_all(bind=engine) # @UndefinedVariable

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


init_exception_handlers(app)

app.include_router(User)
app.include_router(Product)
app.include_router(Stock)
app.include_router(Customer)
# app.include_router(Ai)
app.include_router(AiAgent)

if __name__ == "__main__":
    import uvicorn # @UnresolvedImport
    uvicorn.run(app, host="0.0.0.0", port=8000)
