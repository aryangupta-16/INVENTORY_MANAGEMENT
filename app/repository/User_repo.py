from sqlalchemy.orm import Session # @UnresolvedImport
from app.model.User import User
from app.schema.UserSchema import UserCreate, UserUpdate
from app.utils.password import hash_password

def create_user(user: UserCreate, db: Session):
    hashed_password = hash_password(user.password)
    db_user = User(name=user.name, email=user.email, password=hashed_password, phone=user.phone)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db:Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db:Session):
    return db.query(User).all()

def update_user(db:Session, user_id:int, user:UserUpdate):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    if user.name:
        db_user.name = user.name
    if user.email:
        db_user.email = user.email
    if user.phone:
        db_user.phone = user.phone
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db:Session,user_id:int):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return True