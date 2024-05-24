# shortener_app/main.py

import string
import secrets
import validators

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine
from .keygen import KeyGen
from .key_validation import KeyValidation
from .app_exceptions import AppExceptions
from .crud import CRUD


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return "Welcome to the URL shortener API :)"


@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, alias: str = None, db: Session = Depends(get_db)):
    key_validation = KeyValidation(db)
    crud = CRUD(db)

    url = key_validation.format_url(url)

    if not validators.url(url):
        AppExceptions.raise_bad_request(message="Your provided URL is not valid")

    if alias and not key_validation.validate_key(key=alias, validation_col=models.URL.key):
        AppExceptions.raise_conflict(message="The alias you requested is not available")

    key = alias if alias else key_validation.generate_key()
    secret_key = key_validation.generate_secret_key(key)

    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )

    crud.add_db_url(db_url)
    db_url.url = key
    db_url.admin_url = secret_key

    return db_url



