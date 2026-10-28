from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import APIRouter, Depends, status
from ..schemas import BannedPhrasesCreate, BannedPhrasesResponse, BannedPhrasesUpdate
from ..services.banned_phrase_service import BannedPhraseService
from ..repositories.banned_phrase_repository import BannedPhraseRepository

router = APIRouter(prefix="/api/v1/banned-phrases", tags=["Banned Phrases"])


def get_banned_phrase_service(db: Session = Depends(get_db)) -> BannedPhraseService:
    repo = BannedPhraseRepository(db)
    return BannedPhraseService(repo)


@router.get("", response_model=list[BannedPhrasesResponse])
def get_banned_phrases(
    service: BannedPhraseService = Depends(get_banned_phrase_service),
):
    return service.get_all()


@router.post(
    "", response_model=BannedPhrasesResponse, status_code=status.HTTP_201_CREATED
)
def create_banned_phrases(
    phrase: BannedPhrasesCreate,
    service: BannedPhraseService = Depends(get_banned_phrase_service),
):
    return service.create(phrase)


@router.put("/{id}", response_model=BannedPhrasesResponse)
def update_banned_phrases(
    id: int,
    update: BannedPhrasesUpdate,
    service: BannedPhraseService = Depends(get_banned_phrase_service),
):
    return service.update(id, update)


@router.delete("/{id}")
def delete_banned_phrases(
    id: int, service: BannedPhraseService = Depends(get_banned_phrase_service)
):
    return service.delete(id)
