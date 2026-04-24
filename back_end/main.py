from fastapi import FastAPI
from database import engine
import models
from routers import auth, users, quests, skills, shop, inventory

app = FastAPI(title="Gamified Habit Tracker API")

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(quests.router)
app.include_router(skills.router)
app.include_router(shop.router)
app.include_router(inventory.router)