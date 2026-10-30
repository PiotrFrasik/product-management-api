from sqlalchemy.orm import Session
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

    def update(
        self, product: Product, history_list: list[ProductChangeHistory]
    ) -> Product:
        if history_list:
            for product_history in history_list:
                self.db.add(product_history)

        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product):
        self.db.delete(product)
        self.db.commit()
