from fastapi import HTTPException
from ..repositories.banned_phrase_repository import BannedPhraseRepository
from ..models import BannedPhrase
from ..schemas import BannedPhrasesCreate, BannedPhrasesUpdate


class BannedPhraseService:
    def __init__(self, repository: BannedPhraseRepository):
        self.repository = repository

    def get_all(self) -> list[BannedPhrase]:
        return self.repository.get_all()

    def get_by_id(self, id: int) -> BannedPhrase:
        phrase = self.repository.get_by_id(id)
        if not phrase:
            raise HTTPException(404, f"Phrase {id} not found.")
        return phrase

    def create(self, phrase_data: BannedPhrasesCreate) -> BannedPhrase:
        existing_phrase = self.repository.get_by_name(phrase_data.name)
        if existing_phrase:
            raise HTTPException(status_code=400, detail="The phrase is already taken.")

        db_phrase = BannedPhrase(**phrase_data.model_dump())
        return self.repository.create(db_phrase)

    def update(self, id: int, update_data: BannedPhrasesUpdate) -> BannedPhrase:
        phrase = self.get_by_id(id)

        update_dict = update_data.model_dump(exclude_unset=True)

        if "name" in update_dict:
            new_name = update_dict["name"]
            existing_phrase = self.repository.get_by_name_other_id(new_name, id)
            if existing_phrase:
                raise HTTPException(
                    status_code=400, detail="The phrase is already taken."
                )

        for field, value in update_dict.items():
            setattr(phrase, field, value)

        return self.repository.update(phrase)

    def delete(self, id: int) -> dict[str, str]:
        phrase = self.get_by_id(id)
        self.repository.delete(phrase)
        return {"message": "Phrase deleted"}
