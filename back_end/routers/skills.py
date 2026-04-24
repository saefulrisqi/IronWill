from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import SkillCreate, SkillResponse
from ..crud import create_skill, get_user_skills
from .auth import get_current_user

router = APIRouter(prefix="/skills", tags=["skills"])


@router.post("/", response_model=SkillResponse)
def create_new_skill(
    skill_data: SkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_skill(
        db=db,
        user_id=current_user.id,
        name=skill_data.name,
        parent_skill_id=skill_data.parent_skill_id,
    )


@router.get("/", response_model=list[SkillResponse])
def list_user_skills(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_skills(db=db, user_id=current_user.id)