from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True


class UserCreate(BaseSchema):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, value: str) -> str:
        if not value.replace("_", "").replace("-", "").isalnum():
            raise ValueError("username must be alphanumeric with underscores or hyphens only")
        return value


class UserResponse(BaseSchema):
    id: int
    username: str
    level: int
    total_exp: int
    total_gold: int


class SkillCreate(BaseSchema):
    name: str = Field(..., min_length=1, max_length=100)
    parent_skill_id: Optional[int] = None


class SkillResponse(BaseSchema):
    id: int
    user_id: int
    name: str
    level: int
    exp: int
    parent_skill_id: Optional[int] = None


class QuestCreate(BaseSchema):
    title: str = Field(..., min_length=1, max_length=200)
    difficulty: int = Field(..., ge=1, le=5)
    target_skill_id: Optional[int] = None


class QuestResponse(BaseSchema):
    id: int
    user_id: int
    title: str
    difficulty: int
    target_skill_id: Optional[int] = None


class QuestLogCreate(BaseSchema):
    quest_id: int
    status: str = Field(..., pattern="^(completed|failed)$")


class QuestLogResponse(BaseSchema):
    id: int
    quest_id: int
    status: str
    created_at: datetime


class ShopItemCreate(BaseSchema):
    name: str = Field(..., min_length=1, max_length=100)
    price_gold: int = Field(..., ge=0)
    description: Optional[str] = Field(None, max_length=500)


class ShopItemResponse(BaseSchema):
    id: int
    name: str
    price_gold: int
    description: Optional[str] = None


class InventoryResponse(BaseSchema):
    id: int
    user_id: int
    item_id: int
    quantity: int


class Token(BaseSchema):
    access_token: str
    token_type: str


class TokenData(BaseSchema):
    username: Optional[str] = None