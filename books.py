from fastapi import FastAPI, HTTPException, Request, status,Form,Header
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from starlette.responses import JSONResponse

app=FastAPI()


class NegativeNumberException(Exception):
    def __init__(self,books_to_return):
        self.books_to_return=books_to_return
        

class BOOK(BaseModel):
    id:UUID
    title:str=Field(min_length=1)
    author:str=Field(min_length=1,max_length=25)
    description:str=Field(title="Description of the book",max_length=100,min_length=1)
    rating:Optional[int]=Field(gt=-1,lt=100)
    class Config:
        schema_extra={
            "example":{
                "id":"ee65f376-df6e-11ec-9d64-0242ac120002",
                "title":"Computer Engineering",
                "author":"Juanes",
                "description":"My description",
                "rating":100
            }
        }
class BooksNoRating(BaseModel):
    id:UUID
    title:str=Field(min_length=1)
    author:str
    description:Optional[str]=Field(None,title="Description of the book",max_length=100,min_length=1)


BOOKS=[]
#uvicorn file:app --reload
#endpoints

@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request:Request,exception:NegativeNumberException):
    return JSONResponse(status_code=418,content={"Message":f"Hey!, why do you want {exception.books_to_return} books?. You need to read more!"})

@app.get('/')
async def read_all_books(books_to_return:Optional[int]=None):
    if books_to_return and books_to_return<0:
        raise NegativeNumberException(books_to_return=books_to_return)
    if len(BOOKS)<1:
        create_books_noAPI()
    
    if books_to_return and len(BOOKS)>=books_to_return >0:
        i=1
        new_books=[]
        while i <= books_to_return:
            new_books.append(BOOKS[i-1])
            i+=1
        return new_books
        
    return BOOKS

@app.get("/book/{book_id}")
async def read_book(book_id:UUID):
    for _ in BOOKS:
        if _.id==book_id:
            return _
    raise raise_not_found_exception()

@app.get("/book/rating/{book_id}",response_model=BooksNoRating)
async def read_book_no_rating(book_id:UUID):
    for _ in BOOKS:
        if _.id==book_id:
            return _
    raise raise_not_found_exception()

@app.get("/header")
async def readHeader(random_header:Optional[str]=Header(None)):
    return {"Random header":random_header}

@app.post('/',status_code=status.HTTP_201_CREATED)
async def create_book(book:BOOK):
    BOOKS.append(book)
    return book

@app.post("/books/login")
# async def book_login(book_id:int,username:str=Form(),password:str=Form()):
async def book_login(book_id:int,username:Optional[str]=Header(None),password:Optional[str]=Header(None)):
    if username=="FastAPIUser" and password=="Test1234":
        return BOOKS[book_id]
    return "Invalid User."
@app.put("/{book_id}")
async def update_book(book_id:UUID,book:BOOK):
    counter=0
    for x in BOOKS:
        counter+=1
        if x.id==book_id:
            BOOKS[counter-1]=book
        return BOOKS[counter-1]
    raise raise_not_found_exception()
@app.delete("/{book_id}")
async def delete_book(book_id:UUID):
    counter=0
    for x in BOOKS:
        if x.id==book_id:
            del BOOKS[counter-1]
            return f"ID: {book_id} deleted."
    raise raise_not_found_exception()

def create_books_noAPI():
    book_1=BOOK(
        id="ee65f376-df6e-11ec-9d64-0242ac120002",
        title="Title1",
        author="Author1",description="description1",rating=60)
    book_2=BOOK(
        id="ee65f376-df6e-11ec-9d64-0242ac120002",
        title="Title2",
        author="Author2",description="description2",rating=70)
    book_3=BOOK(
        id="ee65f376-df6e-11ec-9d64-0242ac120002",
        title="Title3",
        author="Author3",description="description3",rating=80)
    book_4=BOOK(
        id="ee65f376-df6e-11ec-9d64-0242ac120002",
        title="Title4",
        author="Author4",description="description4",rating=90)
    book_5=BOOK(
        id="ee65f376-df6e-11ec-9d64-0242ac120002",
        title="Title5",
        author="Author5",description="description5",rating=75)
    
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)
    BOOKS.append(book_5)

def raise_not_found_exception():
    return HTTPException(status_code=404,detail="BOOK not found",headers={"X-Header-Error":"Nothing to seen at the UUID"})