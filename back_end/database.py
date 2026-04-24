from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv  
load_dotenv()

DATABASE_HBT = os.getenv(
    "DATABASE_HBT",
    "postgresql://habit_admin:rahasia123@localhost:5432/habit_db" 
)

engine = create_engine(
    DATABASE_HBT,
    pool_pre_ping=True,
    pool_recycle=300
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()