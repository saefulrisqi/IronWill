from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Index
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    level = Column(Integer, default=1, nullable=False)
    total_exp = Column(Integer, default=0, nullable=False)
    total_gold = Column(Integer, default=0, nullable=False)

    skills = relationship("Skill", back_populates="owner", cascade="all, delete-orphan")
    quests = relationship("Quest", back_populates="owner", cascade="all, delete-orphan")
    inventory_items = relationship("Inventory", back_populates="owner", cascade="all, delete-orphan")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    level = Column(Integer, default=1, nullable=False)
    exp = Column(Integer, default=0, nullable=False)
    parent_skill_id = Column(Integer, ForeignKey("skills.id", ondelete="SET NULL"), nullable=True, index=True)

    owner = relationship("User", back_populates="skills")
    parent_skill = relationship("Skill", remote_side=[id], back_populates="child_skills")
    child_skills = relationship("Skill", back_populates="parent_skill")
    targeted_quests = relationship("Quest", back_populates="target_skill")


class Quest(Base):
    __tablename__ = "quests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    difficulty = Column(Integer, default=1, nullable=False)
    target_skill_id = Column(Integer, ForeignKey("skills.id", ondelete="SET NULL"), nullable=True, index=True)

    owner = relationship("User", back_populates="quests")
    target_skill = relationship("Skill", back_populates="targeted_quests")
    logs = relationship("QuestLog", back_populates="quest", cascade="all, delete-orphan")


class QuestLog(Base):
    __tablename__ = "quest_logs"

    id = Column(Integer, primary_key=True, index=True)
    quest_id = Column(Integer, ForeignKey("quests.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    quest = relationship("Quest", back_populates="logs")

    __table_args__ = (
        Index("ix_quest_logs_status", "status"),
    )


class ShopItem(Base):
    __tablename__ = "shop_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    price_gold = Column(Integer, nullable=False)
    description = Column(String(500), nullable=True)

    inventory_entries = relationship("Inventory", back_populates="item")


class Inventory(Base):
    __tablename__ = "inventories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    item_id = Column(Integer, ForeignKey("shop_items.id", ondelete="CASCADE"), nullable=False, index=True)
    quantity = Column(Integer, default=1, nullable=False)

    owner = relationship("User", back_populates="inventory_items")
    item = relationship("ShopItem", back_populates="inventory_entries")

    __table_args__ = (
        Index("ix_inventories_user_item", "user_id", "item_id", unique=True),
    )