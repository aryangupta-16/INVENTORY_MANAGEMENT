from app.schema.UserSchema import UserCreate, UserResponse, UserLoginRequest, UserUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session # @UnresolvedImport
from app.config.database import get_db
from app.service import user_service
from fastapi.responses import JSONResponse
from app.utils.security import get_current_user
from typing import List

router = APIRouter(prefix='/users',tags=['Users'])

@router.post('/register',response_model=UserResponse)
def signup(user:UserCreate, db:Session=Depends(get_db)):
    try:
        new_user = user_service.register_user(user, db)
        return new_user
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    
@router.post('/login')
def login(user:UserLoginRequest,db:Session=Depends(get_db)):
    auth_result = user_service.authenticate_user(db,user.email,user.password)
    if not auth_result:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return JSONResponse(content=auth_result)


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return user_service.get_user(db, user_id)


@router.get("/", response_model=List[UserResponse])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # If you want admin-only, check current_user.is_admin here
    return user_service.get_all_users(db, skip, limit)

@router.put("/me", response_model=UserResponse)
def update_me(user_in: UserUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return user_service.update_user(db, current_user.id, user_in)

@router.delete("/me")
def delete_me(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return user_service.delete_user(db, current_user.id)