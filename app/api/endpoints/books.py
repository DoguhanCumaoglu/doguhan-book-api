from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from app.db import schemas, crud
from app.db.database import get_db
from app.api.dependencies import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/", response_model=List[schemas.Book])
@limiter.limit("5/minute")
def read_books(
    request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books


@router.get("/{book_id}", response_model=schemas.Book)
@limiter.limit("5/minute")
def read_book(request: Request, book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return book


@router.post("/", response_model=schemas.Book)
@limiter.limit("5/minute")
def create_book(
    request: Request,
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    return crud.create_book(db=db, book=book)


@router.put("/{book_id}", response_model=schemas.Book)
@limiter.limit("5/minute")
def update_book(
    request: Request,
    book_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return crud.update_book(db=db, book_id=book_id, book=book)


@router.delete("/{book_id}", response_model=schemas.Book)
@limiter.limit("5/minute")
def delete_book(
    request: Request,
    book_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return crud.delete_book(db=db, book_id=book_id)
