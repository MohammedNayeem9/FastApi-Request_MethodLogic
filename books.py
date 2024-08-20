from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


# all books
@app.get("/books")
async def first_api():
    return BOOKS


# Path Parameters
@app.get('/books/{book_title}')
async def read_book(book_title:str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book


#dynamic_param
# @app.get("/books/{dynamic_param}")
# async def read_all_books(dynamic_param: str):
#     return {'dynamic_param': dynamic_param}


# Query Parameters
@app.get("/books/")
async def read_category_by_query(category:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return


# Query Parameters with path as author
@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author:str, category:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() ==  book_author.casefold() and \
        book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
            
    return books_to_return


# FastAPI Project: Post Request
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


# FastAPI Project: Put Request
@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
           BOOKS[i]=updated_book


# FastAPI Project: Delete Request
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title:str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break


# Get all books from a specific author using either Path Parameters or Query Parameters

@app.get("/books/byauthor/{author}")
async def read_books_by_author(author:str):
    books_to_rereturn = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_rereturn.append(book)
            
    return books_to_rereturn