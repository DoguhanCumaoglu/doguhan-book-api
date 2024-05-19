from sqlalchemy.orm import Session
from app.db import models, schemas
from app.core.security import get_password_hash
import random


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db_book.isbn = generate_isbn()
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def update_book(db: Session, book_id: int, book: schemas.BookCreate):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        for key, value in book.dict().items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def validate_username(username: str):
    if 4 <= len(username) <= 11:
        return False
    return True


def validate_password(password: str):
    if len(password) < 4:
        return True
    return False


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_favorite(db: Session, user_id: int, book_id: int):
    db_favorite = models.Favorite(user_id=user_id, book_id=book_id)
    db.add(db_favorite)
    db.commit()
    return db_favorite


def get_favorites(db: Session, user_id: int):
    return db.query(models.Favorite).filter(models.Favorite.user_id == user_id).all()


def delete_favorite(db: Session, user_id: int, book_id: int):
    db_favorite = (
        db.query(models.Favorite)
        .filter(models.Favorite.user_id == user_id, models.Favorite.book_id == book_id)
        .first()
    )
    if db_favorite:
        db.delete(db_favorite)
        db.commit()
    return db_favorite


def generate_isbn():
    return random.randint(
        1000000000000, 9999999999999
    )
