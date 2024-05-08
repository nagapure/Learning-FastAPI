from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import UUID


app = FastAPI()

class Book(BaseModel):
    id : UUID
    title : str = Field(min_length=1)
    author : str = Field(min_length=1, max_length=100)
    description : str = Field(title="Description of book", 
                            min_length=1, 
                            max_length=100,
                            )
    rating : int = Field(gt=0, lte=5)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "9accd35b-c3db-453b-a455-af18fc3bc13c",
                "title": "Harry Potter",
                "author": "Chetan",
                "description": "A novel Harry potter",
                "rating" : 4
            }    
        }


BOOKS = []

@app.get("/")
async def get_all_books(books_to_return : Optional[int] = None):
    if len(BOOKS)<1:
        create_book_no_api()
    
    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books = []
        while i<= books_to_return:
            new_books.append(BOOKS[i - 1])
            i += 1
        return new_books
    return BOOKS

@app.get("/book/{book_id}")
async def get_book_by_id(book_id : UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x


@app.post("/book")
async def create_book(book: Book):
    BOOKS.append(book)
    return book

@app.put("/book/{book_id}")
async def update_book(book_id: UUID, book: Book):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter - 1] = book
            return BOOKS[counter - 1]


@app.delete("/book/{book_id}")
async def delete_book(book_id: UUID):
    counter =0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return f'ID: {book_id} has been deleted'

# @app.post("/book")
# async def create_book(book: Book):
#     if any(existing_book.id == book.id for existing_book in BOOKS):
#         raise HTTPException(
#             status_code=400, detail="A book with this ID already exists."
#         )
#     BOOKS.append(book)
#     return book

def create_book_no_api():
    book_1 = Book(
        id = "80aeca47-d9c0-4b16-b88e-d8fdeafed64f",
        title = "On the Road",
        author = "Jack Kerouac",
        description = "A novel about roads",
        rating = 5
    )
    book_2 = Book(
        id = "3accd35b-c3db-453b-a455-af18fc3bc13c",
        title = "Title 2",
        author = "Author 2",
        description = "description 2",
        rating = 3
    )
    book_3 = Book(
        id = "3ec04f36-49d4-42b3-be64-9808c7267f15",
        title = "Title 3",
        author = "Author 3",
        description = "description 3",
        rating = 4
    )

    book_4 = Book(
        id = "4ec04f36-49d4-42b3-be64-9808c7267f15",
        title = "Title 4",
        author = "Author 4",
        description = "description 4",
        rating = 1
    )
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)

    return BOOKS