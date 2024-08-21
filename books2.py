from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

# create a book class
class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

# create a book constructor
    def __init__(self,id,title,author,description,rating,published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    id:  Optional[int] =Field(description="Id is not needed", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1900, lt=2024)

# create a book model to use in the post method example value
    model_config = {
        'json_schema_extra':{
            'example':{
                'title':'A new book',
                'author':'Codingwithnayeem',
                'description':'A new book',
                'rating':5,
                'published_date':2021
            }
        }
    }


# Book()      
BOOKS = [
    Book(1,'Computer Science Pro','Codingwithayeem','A very nice book!',5,2021),
    Book(2,'Be Fast with FastAPI','Codingwithnayeem','A great book!',5,2022),
    Book(3,'Master Endpoints','Codingwithnayeem','A awesome book!',5,2023),
    Book(4,'HP1','Author 1','A great book!',2,2000),
    Book(5,'HP2','Author 2','A great book!',2,2001),
    Book(6,'HP3','Author 3','A great book!',2,2002),
]


# get all books
@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

# get book by id
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)): # gt=0 means greater than 0 and it's a required parameter with Path validation
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')


# Post Request before Validation
# @app.post("/books/create_book")
# async def creaet_book(new_book=Body()):
#     BOOKS.append(new_book)


#  Post Request after Validation
@app.post("/books/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    # print(type(new_book))
    BOOKS.append(find_book_id(new_book))


# find book id function  Optional [int] =Field(title="Id is not needed") it'll automaatically adds a number to the last book id
def find_book_id(book:Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id +1
    return book


#  Fetch Books by Rating
@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating:int = Query(gt=0, lt=6)): # gt greater than, lt less than query parameters validation
    book_to_return = []
    for books in BOOKS:
        if books.rating == book_rating:
            book_to_return.append(books)

    return book_to_return


#  Update Book with Put Request
@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False # it will be true if the book is found
    for i  in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True # it will be false if the book is not found

    if book_changed == False: # if book_changed is false then it means that the book is not found
        raise HTTPException(status_code=404, detail='Item not found') # 404 is not found

# Delete Book with Delete Request
@app.delete("/books/delete_book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    book_changed = False # it will be true if the book is found
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break
        book_changed = True # it will be false if the book is not found

    if book_changed == False: # if book_changed is false then it means that the book is not found
        raise HTTPException(status_code=404, detail='Item not found') # 404 is not found


# GET Request method to filter by published_date with path as published_date
@app.get("/books/by_published_date/{published_date}")
async def read_book_by_published_date(published_date: int):
    books_to_return = []
    for books in BOOKS:
        if books.published_date == published_date:
            books_to_return.append(books)

    return books_to_return


# GET Request method to filter by published_date with Query Parameters
@app.get("/books/by_published_date/")
async def read_book_by_published_date(published_date: int = Query(gt=1900, lt=2024)): # Query Parameters with validation
    books_to_return = []
    for books in BOOKS:
        if books.published_date == published_date:
            books_to_return.append(books)

    return books_to_return