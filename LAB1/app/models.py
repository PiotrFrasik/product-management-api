from sqlalchemy import null
from sqlalchemy import ForeignKey
from sqlalchemy import TIMESTAMP
from sqlalchemy import Column, Integer, String, Float, Enum
from .database import Base
from sqlalchemy.sql import func
import enum

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

class ProductCategory(enum.StrEnum):
    ELEKTRONIKA = "Elektornika"
    KSIAZKA = "Ksiazka"
    ODZIEZ = "Odziez"

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True)
    price = Column(Float)
    category = Column(Enum(ProductCategory), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    quantity = Column(Integer, nullable=False, default=0)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)