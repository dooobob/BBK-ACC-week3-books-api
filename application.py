from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db


def create_app(db_engine=engine):
    # Create the database tables when the app starts.
    # This uses the Book model from models.py.
    models.Base.metadata.create_all(bind=db_engine)

    app = FastAPI()

    @app.get("/")
    def home():
        return {"message": "Week 3 SQLAlchemy API is running"}

    @app.get("/books", response_model=list[schemas.BookResponse])
    def get_books(db: Session = Depends(get_db)):
        # response_model tells FastAPI to return a list of BookResponse objects.
        # Read all books from the database.
        books = db.query(models.Book).all()
        return books

    @app.get("/books/{book_id}", response_model=schemas.BookResponse)
    def get_book(book_id: int, db: Session = Depends(get_db)):
        # Find one book by primary key.
        book = db.query(models.Book).filter(models.Book.id == book_id).first()

        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")

        return book

    @app.post("/books", response_model=schemas.BookResponse, status_code=201)
    def create_book(book_data: schemas.BookCreate, db: Session = Depends(get_db)):
        # book_data has already been checked by Pydantic.
        # We can use dot notation because book_data is a BookCreate object.
        book = models.Book(
            title=book_data.title, author=book_data.author, year=book_data.year
        )

        try:
            db.add(book)
            db.commit()
            db.refresh(book)
            return book

        except IntegrityError:
            db.rollback()

    return app
