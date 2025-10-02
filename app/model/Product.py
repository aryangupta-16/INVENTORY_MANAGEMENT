from sqlalchemy import Column,String,Integer, ForeignKey, Float, DateTime # @unresolvedImport
from sqlalchemy.orm import relationship # @unresolvedImport
from app.config.database import Base
from datetime import datetime

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    unit = Column(String, nullable=False)       
    stock = Column(Integer, default=0)          
    threshold = Column(Integer, default=5)      
    
    user_id = Column(Integer, ForeignKey("users.id"))  
    user = relationship("User", back_populates="products")