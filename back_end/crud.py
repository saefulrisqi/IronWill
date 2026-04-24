from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from models import User, Skill, Quest, QuestLog, ShopItem, Inventory

REWARD_TABLE = {
    1: {"exp": 5,  "gold": 3},
    2: {"exp": 10, "gold": 5},
    3: {"exp": 20, "gold": 10},
    4: {"exp": 35, "gold": 18},
    5: {"exp": 50, "gold": 25},
}


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, username: str, hashed_password: str) -> User:
    db_user = User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_quest(db: Session, quest_id: int, user_id: int) -> Quest | None:
    return (
        db.query(Quest)
        .filter(Quest.id == quest_id, Quest.user_id == user_id)
        .first()
    )


def create_quest(
    db: Session,
    user_id: int,
    title: str,
    difficulty: int,
    target_skill_id: int | None = None
) -> Quest:
    db_quest = Quest(
        user_id=user_id,
        title=title,
        difficulty=difficulty,
        target_skill_id=target_skill_id,
    )
    db.add(db_quest)
    db.commit()
    db.refresh(db_quest)
    return db_quest


def complete_quest(db: Session, user_id: int, quest_id: int) -> dict:
    quest = get_quest(db, quest_id, user_id)
    if quest is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quest not found or does not belong to you",
        )

    already_completed = (
        db.query(QuestLog)
        .filter(QuestLog.quest_id == quest_id, QuestLog.status == "completed")
        .first()
    )
    if already_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quest has already been completed",
        )

    reward = REWARD_TABLE.get(quest.difficulty)
    if reward is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid quest difficulty configuration",
        )

    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    try:
        user.total_exp += reward["exp"]
        user.total_gold += reward["gold"]

        new_level = _calculate_level(user.total_exp)
        if new_level > user.level:
            user.level = new_level

        if quest.target_skill_id is not None:
            skill = (
                db.query(Skill)
                .filter(Skill.id == quest.target_skill_id, Skill.user_id == user_id)
                .first()
            )
            if skill is not None:
                skill.exp += reward["exp"]
                skill.level = _calculate_level(skill.exp)

        quest_log = QuestLog(quest_id=quest_id, status="completed")
        db.add(quest_log)
        db.commit()
        db.refresh(quest_log)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to complete quest, transaction rolled back",
        )

    return {
        "quest_id": quest_id,
        "status": "completed",
        "reward_exp": reward["exp"],
        "reward_gold": reward["gold"],
        "user_level": user.level,
        "user_total_exp": user.total_exp,
        "user_total_gold": user.total_gold,
    }


def _calculate_level(total_exp: int) -> int:
    level = 1
    exp_needed = 100
    while total_exp >= exp_needed:
        total_exp -= exp_needed
        level += 1
        exp_needed = int(exp_needed * 1.2)
    return level


def get_user_skills(db: Session, user_id: int):
    return db.query(Skill).filter(Skill.user_id == user_id).all()


def create_skill(
    db: Session,
    user_id: int,
    name: str,
    parent_skill_id: int | None = None
) -> Skill:
    if parent_skill_id is not None:
        parent = (
            db.query(Skill)
            .filter(Skill.id == parent_skill_id, Skill.user_id == user_id)
            .first()
        )
        if parent is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Parent skill not found or does not belong to you",
            )

    db_skill = Skill(user_id=user_id, name=name, parent_skill_id=parent_skill_id)
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill


def get_shop_items(db: Session):
    return db.query(ShopItem).all()


def get_inventory_by_user(db: Session, user_id: int):
    return db.query(Inventory).filter(Inventory.user_id == user_id).all()


def buy_item(db: Session, user_id: int, item_id: int) -> Inventory:
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    item = db.query(ShopItem).filter(ShopItem.id == item_id).first()
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    if user.total_gold < item.price_gold:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient gold",
        )

    inventory_entry = (
        db.query(Inventory)
        .filter(Inventory.user_id == user_id, Inventory.item_id == item_id)
        .first()
    )

    if inventory_entry:
        inventory_entry.quantity += 1
    else:
        inventory_entry = Inventory(user_id=user_id, item_id=item_id, quantity=1)
        db.add(inventory_entry)

    user.total_gold -= item.price_gold
    db.commit()
    db.refresh(inventory_entry)
    db.refresh(user)
    return inventory_entry