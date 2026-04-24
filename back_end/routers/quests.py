from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import QuestCreate, QuestResponse
from crud import create_quest, complete_quest
from routers.auth import get_current_user

router = APIRouter(prefix="/quests", tags=["quests"])


@router.post("/", response_model=QuestResponse)
def create_new_quest(
    quest_data: QuestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_quest(
        db=db,
        user_id=current_user.id,
        title=quest_data.title,
        difficulty=quest_data.difficulty,
        target_skill_id=quest_data.target_skill_id,
    )


@router.post("/{quest_id}/complete")
def finish_quest(
    quest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return complete_quest(db=db, user_id=current_user.id, quest_id=quest_id)