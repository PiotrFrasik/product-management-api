from fastapi import FastAPI
from . import models, database
from .routers import products, banned_phrases

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(products.router)
app.include_router(banned_phrases.router)
