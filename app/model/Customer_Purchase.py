from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime # @unresolvedImport
from sqlalchemy.orm import relationship # @unresolvedImport
from datetime import datetime
from app.config.database import Base

class CustomerPurchase(Base):
    __tablename__ = "customer_purchases"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="purchases")
    product = relationship("Product")
