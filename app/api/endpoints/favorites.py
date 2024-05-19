from fastapi import APIRouter, Depends, HTTPException,Request,status
from sqlalchemy.orm import Session
from typing import List
from app.db import schemas, crud
from app.db.database import get_db
from app.api.dependencies import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter=Limiter(key_func=get_remote_address)




@router.get("/", response_model=List[schemas.Favorite])
def read_favorites(request:Request,db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return crud.get_favorites(db=db, user_id=current_user.id)

@router.post("/{book_id}", response_model=schemas.Favorite)
def create_favorite(request:Request,book_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return crud.create_favorite(db=db, user_id=current_user.id, book_id=book_id)

@router.delete("/{book_id}", response_model=schemas.Favorite)
def delete_favorite(request:Request,book_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_favorite = crud.delete_favorite(db=db, user_id=current_user.id, book_id=book_id)
    if db_favorite is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return db_favorite
