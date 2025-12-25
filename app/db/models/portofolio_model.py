# app/db/models/portofolio_model.py
from sqlalchemy import (Column, Integer, String, ForeignKey, Numeric, Date, Enum, Boolean, TIMESTAMP, func, CHAR, text)
from sqlalchemy.orm import relationship
import enum
from app.db.database import Base


class AccountStatus(enum.Enum):
    Active = "Active"
    Dormant = "Dormant"
    Closed = "Closed"


class PortofolioAccount(Base):
    __tablename__ = "portofolio_accounts"

    portofolio_id = Column(Integer, primary_key=True, autoincrement=True)
    account_number = Column(String(30), unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), unique=True)
    currency_code = Column(CHAR(3), server_default="IDR")
    balance = Column(Numeric(15, 2), server_default="0.00")
    open_date = Column(Date, server_default=text("(CURRENT_DATE())"))
    status = Column(Enum(AccountStatus), server_default="Active")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    customer = relationship(
        "Customer",
        back_populates="portofolio",
        foreign_keys=[customer_id]
    )
    transactions = relationship("Transaction", back_populates="source_account")
    mutations = relationship("Mutation", back_populates="account")
