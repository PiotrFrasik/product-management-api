from sqlalchemy.orm import Session
from ..models import BannedPhrase


class BannedPhraseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[BannedPhrase]:
        return self.db.query(BannedPhrase).all()

    def get_by_id(self, id: int) -> BannedPhrase | None:
        return self.db.query(BannedPhrase).filter(BannedPhrase.id == id).first()

    def get_by_name(self, name: str) -> BannedPhrase | None:
        return self.db.query(BannedPhrase).filter(BannedPhrase.name == name).first()

    def get_by_name_other_id(self, name: str, id: int) -> BannedPhrase | None:
        return (
            self.db.query(BannedPhrase)
            .filter(BannedPhrase.name == name, BannedPhrase.id != id)
            .first()
        )

    def create(self, phrase: BannedPhrase) -> BannedPhrase:
        self.db.add(phrase)
        self.db.commit()
        self.db.refresh(phrase)
        return phrase

    def update(self, phrase: BannedPhrase) -> BannedPhrase:
        self.db.commit()
        self.db.refresh(phrase)
        return phrase

    def delete(self, phrase: BannedPhrase):
        self.db.delete(phrase)
        self.db.commit()
