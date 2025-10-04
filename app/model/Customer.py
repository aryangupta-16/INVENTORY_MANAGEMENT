from sqlalchemy import Column, Integer, String, ForeignKey # @unresolvedImport
from sqlalchemy.orm import relationship # @unresolvedImport
from app.config.database import Base


class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, index = True, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String,nullable=False)
    phone = Column(String,nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="customer")
    purchases = relationship("CustomerPurchase", back_populates="customer")