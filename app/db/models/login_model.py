# app/db/models/login_model.py
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.db.database import Base

class Login(Base):
    __tablename__ = "logins"

    login_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    last_login = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    customer = relationship("Customer", back_populates="login")
