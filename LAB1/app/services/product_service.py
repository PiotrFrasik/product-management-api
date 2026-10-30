from fastapi import HTTPException
from ..repositories.banned_phrase_repository import BannedPhraseRepository
from ..repositories.product_repository import ProductRepository
from ..models import Product, ProductChangeHistory
from ..schemas import ProductUpdate, ProductCreate


class ProductService:
    def __init__(
        self,
        product_repo: ProductRepository,
        banned_phrase_repo: BannedPhraseRepository,
    ):
        self.product_repo = product_repo
        self.banned_phrase_repo = banned_phrase_repo

    def _validate_banned_phrases(self, name: str) -> None:
        """Checks whether the name does not contain any of the banned phrases."""
        banned_phrases = self.banned_phrase_repo.get_all()
        for phrase in banned_phrases:
            if phrase.name.lower() in name.lower():
                raise HTTPException(
                    status_code=400,
                    detail=f"The product name contains banned phrase: '{phrase.name}'.",
                )

    def get_all(self) -> list[Product]:
        return self.product_repo.get_all()

    def get_by_id(self, id: int) -> Product:
        product = self.product_repo.get_by_id(id)
        if not product:
            raise HTTPException(404, f"Product {id} not found.")
        return product

    def get_product_history_by_id(self, id: int) -> list[ProductChangeHistory]:
        if not self.product_repo.get_by_id(id):
            raise HTTPException(404, f"Product {id} not found.")
        return self.product_repo.get_product_history_by_id(id)

    def create(self, product_data: ProductCreate) -> Product:
        existing_product = self.product_repo.get_by_name(product_data.name)
        if existing_product:
            raise HTTPException(
                status_code=400, detail="The product name is already taken."
            )

        self._validate_banned_phrases(product_data.name)

        db_product = Product(**product_data.model_dump())
        return self.product_repo.create(db_product)

    def update(self, id: int, update_data: ProductUpdate) -> Product:
        product = self.get_by_id(id)

        update_dict = update_data.model_dump(exclude_unset=True)

        if "name" in update_dict:
            new_name = update_dict["name"]

            existing_product = self.product_repo.get_by_name_other_id(new_name, id)
            if existing_product:
                raise HTTPException(
                    status_code=400, detail="The product name is already taken."
                )

            self._validate_banned_phrases(new_name)

        for field, value in update_dict.items():
            setattr(product, field, value)

        return self.product_repo.update(product)

    def delete(self, id: int) -> dict[str, str]:
        product = self.get_by_id(id)
        self.product_repo.delete(product)
        return {"message": "Product deleted"}
