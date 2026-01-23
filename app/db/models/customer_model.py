# app/db/models/customer_model.py
from sqlalchemy import Column, Integer, String, Date, Text, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100))
    birth_date = Column(Date)
    address = Column(Text)
    NIK = Column(String(20), unique=True)
    phone_number = Column(String(20))
    email = Column(String(100))
    PIN = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    login = relationship("Login", back_populates="customer", uselist=False)

    # Hubungan ke PortofolioAccount
    portofolio = relationship(
        "PortofolioAccount",
        back_populates="customer",
        uselist=False,
        foreign_keys="PortofolioAccount.customer_id"
    )
