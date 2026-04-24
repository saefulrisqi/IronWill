from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import engine, get_db
import models
from security import verify_password, create_access_token
from crud import get_user_by_username
from schemas import Token
from routers import auth, users, quests, skills, shop, inventory

app = FastAPI(title="Gamified Habit Tracker API")

models.Base.metadata.create_all(bind=engine)


@app.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = get_user_by_username(db, form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(quests.router)
app.include_router(skills.router)
app.include_router(shop.router)
app.include_router(inventory.router)