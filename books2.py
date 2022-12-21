from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from starlette.responses import JSONResponse


class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return


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


class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(
        min_length=1
    )
    author: str
    description: Optional[str] = Field(
        title='Description of the book',
        max_length=100,
        min_length=1
    )


BOOKS = []


@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request: Request, exception: NegativeNumberException):
    return JSONResponse(
        status_code=418,
        content={'message': f'Hey, why do you want {exception.books_to_return}? You need to read more!'}
    )


@app.post("/books/login")
async def book_login(username: str = Form(), password: str = Form()):
    return {
        'username': username,
        'password': password
    }


@app.get("/header")
async def read_header(random_header: Optional[str] = Header(None)):
    return {"Random-Header": random_header}


@app.post("/exercise/books/login/")
async def book_login_exercise(book_to_read: UUID, username: str = Header(None), password: str = Header(None)):
    if username == 'FastAPIUser' and password == 'test1234!':
        return await read_book(book_id=book_to_read)
    else:
        return 'Invalid user'


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return=books_to_return)
    else:
        pass

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


@app.get("/book/{book_id}", response_model=Book)
async def read_book(book_id: UUID):
    for book in BOOKS:
        if book.id == book_id:
            return book
        else:
            continue
    # id not found books to read, raise exception
    raise raise_item_can_not_be_found_exception()


@app.get("/book/rating/{book_id}", response_model=BookNoRating)
async def read_book_no_rating(book_id: UUID):
    for book in BOOKS:
        if book.id == book_id:
            return book
        else:
            continue
    # id not found books to read, raise exception
    raise raise_item_can_not_be_found_exception()


@app.post("/", status_code=status.HTTP_201_CREATED)
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
    # id not found books to update, raise exception
    raise raise_item_can_not_be_found_exception()


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
    # did not return anything because book_id not in books, raise exception
    raise raise_item_can_not_be_found_exception()


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


def raise_item_can_not_be_found_exception():
    return HTTPException(
        status_code=404,
        detail='Book not found',
        headers={'X-Header-Error': 'Nothing to be seen at the UUID'}
    )
