# app/db/models/transaction_model.py
from sqlalchemy import (
    Column, BigInteger, String, Enum, Numeric, CHAR, TIMESTAMP, func, ForeignKey
)
from sqlalchemy.orm import relationship
import enum
from app.db.database import Base


class TransactionType(enum.Enum):
    TrfOnln = "TrfOnln"
    TrfOvrbok = "TrfOvrbok"


class TransactionBank(enum.Enum):
    Internal = "Internal"
    Eksternal = "Eksternal"


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(BigInteger, primary_key=True, autoincrement=True)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    transaction_bank = Column(Enum(TransactionBank), nullable=False)
    bank_reference = Column(String(50))
    source_account_number = Column(String(30), ForeignKey("portofolio_accounts.account_number"))
    target_account_number = Column(String(30))
    amount = Column(Numeric(15, 2), nullable=False)
    currency_code = Column(CHAR(3), server_default="IDR")
    description = Column(String(255))
    transaction_date = Column(TIMESTAMP, server_default=func.current_timestamp())
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    # Relationships
    source_account = relationship("PortofolioAccount", back_populates="transactions")
    mutations = relationship("Mutation", back_populates="transaction")
