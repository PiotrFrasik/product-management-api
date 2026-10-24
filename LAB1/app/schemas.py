from pydantic import ConfigDict
from pydantic import model_validator
from pydantic import BaseModel, EmailStr, Field
from .models import ProductCategory
from datetime import datetime

# USER

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

# PRODUCT

class ProductBase(BaseModel):
    name: str = Field(max_length=20, min_length=3, pattern=r"^[a-zA-Z0-9]+$")
    price: float
    category: ProductCategory
    quantity: int = Field(default=0, ge=0)

    @model_validator(model="after")
    def validate_price_for_category(self):
        limits = {
            ProductCategory.ELEKTRONIKA: (50.0, 50_00.0),
            ProductCategory.KSIAZKA: (5.0, 500.0),
            ProductCategory.ODZIEZ: (10.0, 5_000.0),
        }

        min_p, max_p = limits.get(self.category, (0.0, float("inf"))) 
        if not (min_p <= self.price <= max_p): 
            raise ValueError(
                f"Dla kategorii {self.category.value} cena musi mieścić się w przedziale {min_p} - {max_p} PLN"
            )
            return self

class ProductUpdate(BaseModel):
    name: str | None = Field(max_length=20, min_length=3, pattern=r"^[a-zA-Z0-9]+$")
    price: float | None = None
    category: ProductCategory | None = None
    quantity: int | None = Field(default=0, ge=0)

class ProductResponse(ProductBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)