# app/db/models/mutation_model.py
from sqlalchemy import (
    Column, BigInteger, String, Enum, Numeric, TIMESTAMP, func, ForeignKey
)
from sqlalchemy.orm import relationship
import enum
from app.db.database import Base


class MutationType(enum.Enum):
    Debit = "Debit"
    Kredit = "Kredit"


class Mutation(Base):
    __tablename__ = "mutations"

    mutation_id = Column(BigInteger, primary_key=True, autoincrement=True)
    account_number = Column(String(30), ForeignKey("portofolio_accounts.account_number"))
    transaction_id = Column(BigInteger, ForeignKey("transactions.transaction_id"))
    mutation_type = Column(Enum(MutationType), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    balance_after = Column(Numeric(15, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    # Relationships
    account = relationship("PortofolioAccount", back_populates="mutations")
    transaction = relationship("Transaction", back_populates="mutations")
