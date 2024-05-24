# shortener_app/keygen.py

import secrets
import string

from sqlalchemy.orm import Session

from . import models


class KeyGen:

    LETTERS = string.ascii_letters
    DIGITS = string.digits

    def __int__(self, db: Session):
        self.db = db

    def generate_random_key(self, length: int = 5, digits: bool = False):
        chars = self.LETTERS + self.DIGITS if digits else self.LETTERS
        return "".join(secrets.choice(chars) for _ in range(length))




