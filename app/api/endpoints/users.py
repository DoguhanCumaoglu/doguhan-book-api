from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db import schemas, crud
from app.db.database import get_db
from app.core.security import create_access_token, get_password_hash, verify_password
from app.core.config import settings
from typing import Annotated
from app.api import dependencies
from datetime import timedelta
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.session import Token_Session

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/register")
@limiter.limit("5/minute")
async def register(
    request: Request, user: schemas.UserCreate, db: Session = Depends(get_db)
):
    if crud.validate_username(username=user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The length of the username must be between 4 and 11 characters",
        )

    if crud.validate_password(password=user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 4 characters long",
        )

    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    crud.create_user(db=db, user=user)
    return {"message": "Successfully registered"}


@router.post("/login")
@limiter.limit("5/minute")
async def login_for_access_token(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> schemas.Token:
    user = crud.get_user_by_username(db, username=form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    Token_Session[user.username] = access_token
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.post("/logout")
@limiter.limit("5/minute")
async def logout(
    request: Request,
    current_user: schemas.User = Depends(dependencies.get_current_user),
):
    Token_Session.pop(current_user.username, None)
    return {"message": "Successfully logged out"}
