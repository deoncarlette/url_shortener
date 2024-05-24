# shortener_app/key_validation.py

from sqlalchemy.orm import Session

from . import models
from .keygen import KeyGen


class KeyValidation:

    def __init__(self, db: Session, model: models.URL = models.URL):
        self.db = db
        self.model_url = model
        self.keygen = KeyGen()

    def get_db_url_by_key(self, url_key, validation_col):
        db_url = (
            self.db.query(self.model_url)
            .filter(validation_col == url_key, self.model_url.is_active)
            .first()
        )
        return db_url

    def validate_key(self, key, validation_col):
        if not self.get_db_url_by_key(key, validation_col):
            return True

    def generate_key(self, length=5):
        random_key = self.keygen.generate_random_key(length)

        while not self.validate_key(random_key, validation_col=models.URL.key):
            random_key = self.keygen.generate_random_key(length)

        return random_key

    def generate_secret_key(self, key):
        return f"{key}_{self.keygen.generate_random_key(length=8, digits=True)}"

    @staticmethod
    def format_url(url):
        if url.startswith("http://") or url.startswith("https://"):
            return url
        return "".join(["http://", url])
        # TODO: this is function is not in the right class
