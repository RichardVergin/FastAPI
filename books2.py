from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional


app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(
        min_length=1
    )
    author: str = Field(
        min_length=1,
        max_length=100
    )
    description: Optional[str] = Field(
        title='Description of the book',
        max_length=100,
        min_length=1
    )
    rating: int = Field(
        gt=-1,
        lt=101
    )

    class Config:
        schema_extra = {
            'example': {
                'id': 'f860d1fa-8dfb-4969-aba0-538cffb5a338',
                'title': 'Richies Buch',
                'author': 'Richie',
                'description': 'awesome description',
                'rating': 100
            }
        }


BOOKS = []


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    if len(BOOKS) < 1:
        create_books_no_api()
    else:
        pass

    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(BOOKS[i-1])
            i += 1
        return new_books
    else:
        pass

    return BOOKS


@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for book in BOOKS:
        if book.id == book_id:
            return book
        else:
            continue


@app.post("/")
async def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.put("/{book_id}")
async def update_book(book_id: UUID, updated_book: Book):
    counter = 0

    for book in BOOKS:
        counter += 1
        if book.id == book_id:
            BOOKS[counter - 1] = updated_book
            return BOOKS[counter - 1]
        else:
            continue


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0

    for book in BOOKS:
        counter += 1
        if book.id == book_id:
            del BOOKS[counter - 1]
            return f'ID: {book_id} deleted'
        else:
            continue


def create_books_no_api():
    book_1 = Book(
        id='11991961-f9a8-46fe-a19b-3e5bcfbc03e9',
        title='Title 1',
        author='Author 1',
        description='Description 1',
        rating=60
    )
    book_2 = Book(
        id='c881ba31-7de4-4781-a1ce-226f68d61983',
        title='Title 2',
        author='Author 2',
        description='Description 2',
        rating=70
    )
    book_3 = Book(
        id='e42a2c9e-6746-49b9-83c1-6ee0dce18b6e',
        title='Title 3',
        author='Author 3',
        description='Description 3',
        rating=80
    )
    book_4 = Book(
        id='857fae6a-8b7d-4697-899c-01a2fce56fac',
        title='Title 4',
        author='Author 4',
        description='Description 4',
        rating=90
    )
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)
