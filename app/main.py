from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.User_route import router as User
from app.api.Product_route import router as Product
from app.config.database import engine, Base

app = FastAPI()

# Base.metadata.drop_all(bind=engine) # @UndefinedVariable
Base.metadata.create_all(bind=engine) # @UndefinedVariable

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(User)
app.include_router(Product)

if __name__ == "__main__":
    import uvicorn # @UnresolvedImport
    uvicorn.run(app, host="0.0.0.0", port=8000)
