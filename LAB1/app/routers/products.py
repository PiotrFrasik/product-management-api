from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import ProductCreate, ProductResponse, ProductUpdate
from ..services.product_service import ProductService
from ..repositories.product_repository import ProductRepository
from ..repositories.banned_phrase_repository import BannedPhraseRepository

router = APIRouter(prefix="/api/v1/products", tags=["Products"])


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    product_repo = ProductRepository(db)
    banned_phrase_repo = BannedPhraseRepository(db)
    return ProductService(product_repo, banned_phrase_repo)


@router.get("", response_model=list[ProductResponse])
def get_products(service: ProductService = Depends(get_product_service)):
    return service.get_all()


@router.get("/{id}", response_model=ProductResponse)
def get_product(id: int, service: ProductService = Depends(get_product_service)):
    return service.get_by_id(id)


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate, service: ProductService = Depends(get_product_service)
):
    return service.create(product)


@router.put("/{id}", response_model=ProductResponse)
def update_product(
    id: int,
    update: ProductUpdate,
    service: ProductService = Depends(get_product_service),
):
    return service.update(id, update)


@router.delete("/{id}")
def delete_product(id: int, service: ProductService = Depends(get_product_service)):
    return service.delete(id)
