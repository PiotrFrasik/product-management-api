from sqlalchemy import TIMESTAMP, Column, Integer, String, Float, Enum
from sqlalchemy.sql import func
import enum
from .database import Base


class ProductCategory(enum.StrEnum):
    ELEKTRONIKA = "Elektronika"
    KSIAZKA = "Ksiazka"
    ODZIEZ = "Odziez"


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True)
    price = Column(Float)
    category = Column(Enum(ProductCategory), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    quantity = Column(Integer, nullable=False, default=0)


class BannedPhrase(Base):
    __tablename__ = "banned_phrase"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
