from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, model_validator, field_validator
from .models import ProductCategory


class ProductBase(BaseModel):
    name: str = Field(min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9]+$")
    price: float
    category: ProductCategory
    quantity: int = Field(default=0, ge=0)

    @field_validator("quantity", mode="before")
    @classmethod
    def validate_quantity(cls, v):
        if not isinstance(v, int):
            raise ValueError(
                "Quantity must be an integer. Please correct the quantity field."
            )
        if v < 0:
            raise ValueError(
                "Quantity cannot be less than zero. Please correct the quantity field."
            )
        return v

    @model_validator(mode="after")
    def validate_price_for_category(self):
        limits = {
            ProductCategory.ELEKTRONIKA: (50.0, 50_000.0),
            ProductCategory.KSIAZKA: (5.0, 500.0),
            ProductCategory.ODZIEZ: (10.0, 5_000.0),
        }

        min_p, max_p = limits.get(self.category, (0.0, float("inf")))
        if not (min_p <= self.price <= max_p):
            raise ValueError(
                f"For category {self.category.value}, the price must be between {min_p} and {max_p} PLN."
            )

        return self


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(
        default=None, min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9]+$"
    )
    price: float | None = None
    category: ProductCategory | None = None
    quantity: int | None = Field(default=None, ge=0)


class ProductResponse(ProductBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BannedPhrasesBase(BaseModel):
    name: str = Field(min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9 ]+$")


class BannedPhrasesCreate(BannedPhrasesBase):
    pass


class BannedPhrasesUpdate(BannedPhrasesBase):
    pass


class BannedPhrasesResponse(BannedPhrasesBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductChangeHistoryResponse(BaseModel):
    id: int
    id_product: int
    variable_name: str
    old_value: str | None = None
    new_value: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
