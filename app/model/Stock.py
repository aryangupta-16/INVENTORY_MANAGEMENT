from app.config.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime # @unresolvedImport
from sqlalchemy.orm import relationship # @unresolvedImport
from datetime import datetime


class Stock(Base):
    __tablename__ = "stocks"
    
    id = Column(Integer,primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    change = Column(Integer, nullable=False) 
    reason = Column(String, nullable=True)   
    created_at = Column(DateTime, default=datetime.utcnow)
    
    product = relationship("Product")
    user = relationship("User")