from sqlalchemy.orm import Session
from sqlalchemy import inspect, Enum
from ..models import Product, ProductChangeHistory, ProductCategory


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Product]:
        return self.db.query(Product).all()

    def get_by_id(self, id: int) -> Product | None:
        return self.db.query(Product).filter(Product.id == id).first()

    def get_by_name(self, name: str) -> Product | None:
        return self.db.query(Product).filter(Product.name == name).first()

    def get_by_name_other_id(self, name: str, id: int) -> Product | None:
        return (
            self.db.query(Product)
            .filter(Product.name == name, Product.id != id)
            .first()
        )

    def get_product_history_by_id(self, id: int) -> list[ProductChangeHistory] | None:
        return (
            self.db.query(ProductChangeHistory)
            .filter(ProductChangeHistory.id_product == id)
            .all()
        )

    def create(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update(self, product: Product) -> Product:
        state = inspect(product)
        if state.modified:
            for attr in state.attrs:
                history = attr.history
                if history.has_changes():
                    old_value = history.deleted[0] if history.deleted else None
                    new_value = history.added[0] if history.added else None

                    if isinstance(old_value, Enum):
                        old_value = old_value.value

                    if isinstance(new_value, Enum):
                        new_value = new_value.value

                    new_producy_history = ProductChangeHistory(
                        id_product=product.id,
                        variable_name=str(attr.key),
                        old_value=str(old_value) if old_value is not None else None,
                        new_value=str(new_value),
                    )
                    self.db.add(new_producy_history)

        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product):
        self.db.delete(product)
        self.db.commit()
