from sqlalchemy import Column,String,Integer,Boolean # @unresolvedImport
from sqlalchemy.orm import relationship # @unresolvedImport
from app.config.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String) 
    email = Column(String, unique=True)
    password = Column(String)
    phone = Column(String, nullable=True)
    
    products = relationship("Product", back_populates="user")