from passlib.context import CryptContext # @unresolvedImport

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str) -> str:
    print("Hashing password:", password)
    return pwd_context.hash(password)

def verify_password(password:str,hashed_password) -> bool:
    return pwd_context.verify(password,hashed_password)