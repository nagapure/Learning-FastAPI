from enum import Enum
from typing import Optional
from fastapi import FastAPI



app = FastAPI()

BOOKS = {
    'book_1':{'title': 'On the Road', 'author': 'Jack Kerouac'},
    'book_2':{'title': 'Title Two', 'author': 'Author Two'},
    'book_3':{'title': 'Title Three', 'author': 'Author Three'},
    'book_4':{'title': 'Title Four', 'author': 'Author Four'},
    'book_5':{'title': 'Title Five', 'author': 'Author Five'},
    
}

class DirectionName(str, Enum):
    north = "North"
    south = "South"
    east = "East"
    west = "West"


@app.get("/")
async def read_all_books():
    return BOOKS


@app.get("/skip_book")
async def read_all_books(skip_book: Optional[str] = None):
    if skip_book:
        new_books = BOOKS.copy()
        del new_books[skip_book]
        return new_books
    return BOOKS 

# @app.get("/book/{book_id}")
# async def read_book(book_id : int):
#     return {"book_title": book_id}

@app.get("/direction/{direction_name}")
async def get_direction(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        return {"direction": direction_name, "sub":"Up"}
    if direction_name == DirectionName.south:
        return {"direction": direction_name, "sub":"Down"}
    if direction_name == DirectionName.east:
        return {"direction": direction_name, "sub":"Left"}
    if direction_name == DirectionName.west:
        return {"direction": direction_name, "sub":"Right"}
    else:
        return {"direction": "unknown"}
    

@app.get("/book/{book_name}")
async def read_book(book_name: str):
    return BOOKS[book_name]

@app.post("/")
async def create_book(book_title, book_author):
    current_book_id = 0

    if len(BOOKS)>0:
        for book in BOOKS:
            x = int(book.split('_')[-1])
            if x > current_book_id:
                current_book_id = x
    
    BOOKS[f'book_{current_book_id+1}'] = {'title': book_title, 'author': book_author}
    return BOOKS[f'book_{current_book_id+1}']

@app.put("/{book_name}")
async def update_book(book_name: str, book_title: str, book_author: str):
    book_information = {"title": book_title, "author": book_author}
    BOOKS[book_name] = book_information
    return book_information

@app.delete("/{book_name}")
async def delete_book(book_name: str):
    del BOOKS[book_name]
    return f'Book_{book_name} deleted'

'''
1. Create a new read book function that uses query params instead of path params.
2. Create a new delete book function that uses query params instead of path params.
'''

@app.get("/assignment/")
async def read_book_assignment(book_name: str):
    return BOOKS[book_name]

@app.delete("/assignment/")
async def delete_book_assignment(book_name: str):
    del BOOKS[book_name]
    return BOOKS