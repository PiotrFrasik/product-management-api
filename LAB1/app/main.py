from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, database, schemas
from sqlalchemy import func

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/v1/products", response_model=list[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()


@app.get("/api/v1/products/{id}", response_model=schemas.ProductResponse)
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(404, f"Product {id} not found.")
    return product


@app.post("/api/v1/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):

    existing_product = (
        db.query(models.Product).filter(models.Product.name == product.name).first()
    )
    if existing_product:
        raise HTTPException(
            status_code=400, detail="The product name is already taken."
        )

    banned_phrases = db.query(models.BannedPhrase).all()

    for phrase in banned_phrases:
        if phrase.name.lower() in product.name.lower():
            raise HTTPException(
                status_code=400,
                detail=f"The product name contains banned phrase: '{phrase.name}'.",
            )

    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.put("/api/v1/products/{id}", response_model=schemas.ProductResponse)
def update_product(
    id: int, update: schemas.ProductUpdate, db: Session = Depends(get_db)
):

    product = db.query(models.Product).filter(models.Product.id == id).first()

    if not product:
        raise HTTPException(404, f"Product {id} not found.")

    # Get field if is not None
    update_data = update.model_dump(exclude_unset=True)

    if "name" in update_data:
        new_name = update_data["name"]

        existing_product = (
            db.query(models.Product)
            .filter(models.Product.name == new_name, models.Product.id != id)
            .first()
        )
        if existing_product:
            raise HTTPException(
                status_code=400, detail="The product name is already taken."
            )

        banned_phrases = db.query(models.BannedPhrase).all()

        for phrase in banned_phrases:
            if phrase.name.lower() in new_name.lower():
                raise HTTPException(
                    status_code=400,
                    detail=f"The product name contains banned phrase: '{phrase.name}'.",
                )

    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


@app.delete("/api/v1/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(404, f"Product {id} not found.")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}


# ====== Banned Phrases ======


@app.get("/api/v1/banned-phrases", response_model=list[schemas.BannedPhrasesResponse])
def get_banned_phrases(db: Session = Depends(get_db)):
    return db.query(models.BannedPhrase).all()


@app.post("/api/v1/banned-phrases", response_model=schemas.BannedPhrasesResponse)
def create_banned_phrases(
    phrase: schemas.BannedPhrasesCreate, db: Session = Depends(get_db)
):

    existing_phrase = (
        db.query(models.BannedPhrase)
        .filter(models.BannedPhrase.name == phrase.name)
        .first()
    )
    if existing_phrase:
        raise HTTPException(status_code=400, detail="The phrase is already taken.")

    db_phrases = models.BannedPhrase(**phrase.model_dump())
    db.add(db_phrases)
    db.commit()
    db.refresh(db_phrases)
    return db_phrases


@app.put("/api/v1/banned-phrases/{id}", response_model=schemas.BannedPhrasesResponse)
def update_banned_phrase(
    id: int, update: schemas.BannedPhrasesUpdate, db: Session = Depends(get_db)
):
    phrase = db.query(models.BannedPhrase).filter(models.BannedPhrase.id == id).first()

    if not phrase:
        raise HTTPException(404, f"Phrase {id} not found.")

    # Get field if is not None
    update_data = update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(phrase, field, value)

    db.commit()
    db.refresh(phrase)
    return phrase


@app.delete("/api/v1/banned-phrases/{id}")
def delete_banned_phrase(id: int, db: Session = Depends(get_db)):
    phrase = db.query(models.BannedPhrase).filter(models.BannedPhrase.id == id).first()
    if not phrase:
        raise HTTPException(404, f"Banned phrase {id} not found.")
    db.delete(phrase)
    db.commit()
    return {"message": "Phrase deleted"}