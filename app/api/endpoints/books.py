from fastapi import APIRouter, Depends, HTTPException,status,Request
from sqlalchemy.orm import Session
from typing import List
from app.db import schemas, crud
from app.db.database import get_db
from app.api.dependencies import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


limiter = Limiter(key_func=get_remote_address)

router = APIRouter()



@router.get("/", response_model=List[schemas.Book])
@limiter.limit("5/minute")
def read_books(request: Request , db: Session = Depends(get_db)):  # with limit and offset you can make pagination.
    books = crud.get_books(db)
    return books

@router.get("/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book not found")
    return book

@router.post("/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return crud.create_book(db=db, book=book)

@router.put("/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_BAD_REQUEST, detail="Book not found")
    return crud.update_book(db=db, book_id=book_id, book=book)

@router.delete("/{book_id}", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_BAD_REQUEST, detail="Book not found")
    return crud.delete_book(db=db, book_id=book_id)
