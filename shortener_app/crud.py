# shortener_app/crud.py

from sqlalchemy.orm import Session


class CRUD:

    def __int__(self, db: Session):
        self.db = db

    def add_db_url(self, url):

        self.db.add(url)
        self.db.commit()
        self.db.refresh(url)

