from sqlalchemy.orm import Session # @UnresolvedImport
from app.schema.UserSchema import UserCreate
from app.utils.security import create_access_token
from app.utils.password import verify_password
from app.repository.User_repo import get_user_by_email, create_user, get_user_by_id, get_all_users as get_users, update_user as update_user_in_db, delete_user as delete_user_in_db
from fastapi import HTTPException, status
from app.schema.UserSchema import UserUpdate
from app.utils.password import hash_password

def register_user(user: UserCreate, db: Session):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise ValueError("Email already registered")
    return create_user(user, db)

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        return None
    
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token-type": "bearer"}

def get_user(db: Session, user_id: int):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return get_users(db)

def update_user(db: Session, user_id: int, user_in: UserUpdate):
    # hashed_password = None
    # if user_in.password:
    #     hashed_password = hash_password(user_in.password)
    updated = update_user_in_db(db, user_id, user_in)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated

def delete_user(db: Session, user_id: int):
    ok = delete_user_in_db(db, user_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "User deleted successfully"}

