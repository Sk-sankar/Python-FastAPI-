from fastapi import FastAPI,Path,Query,HTTPException
from pydantic import BaseModel,Field
from typing import Optional
from starlette import status

app=FastAPI()

class Book:
    id:int
    title:str
    author:str
    description:str
    rating:int
    published_date:int
    
    def __init__(self,id,title,author,description,rating,published_date):
        self.id=id  
        self.title=title
        self.author=author
        self.description=description
        self.rating=rating
        self.published_date=published_date
        

class BookRequest(BaseModel):
    id:Optional[int]=Field(description="The id not  of the book",default=None)
    title:str=Field(min_length=3)
    author:str=Field(min_length=3)
    description:str = Field(min_length=3,max_length=100)
    rating:int=Field(gt=1,lt=5)
    published_date:int=Field(description="The date the book was published",default=None)
    
    model_config={
        "json_schema_extra": {
            "example": {
                "title": "Title One",
                "author": "Author One",
                "description": "Description One",
                "rating": 5,
                "published_date":2000
            }
        }
    }
    

BOOKS=[
    Book(1,'Title One','Author One','Description One',5,2012),
    Book(2,'Title Two','Author Two','Description Two',4,2022),
    Book(3,'Title Three','Author Three','Description Three',3,2015),
    Book(4,'Title Four','Author Four','Description Four',2,2018),
    Book(5,'Title Five','Author Five','Description Four',1,2019),
]

@app.get("/books",status_code=status.HTTP_200_OK)

async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}")

async def read_book_by_id(book_id:int=Path(gt=0) ):
    for book in BOOKS:
        if book.id==book_id:
            return book
    raise HTTPException(status_code=404,detail="status deos not working")
        
        
        
        
    
@app.get("books/",status_code=status.HTTP_200_OK)

async def read_by_published_date(published_date:int=Query(gt=2000,lt=2022)):  
    book_return=[]
    for book in BOOKS:
        if book.published_date==published_date:
            book_return.append(book)
    return book_return

@app.get("/books/",status_code=status.HTTP_200_OK)
async def read_by_rating(book_rating:int=Query(gt=0,lt=5)):
    book_return=[]
    for book in BOOKS:
        if book.rating==book_rating:
            book_return.append(book)
    return book_return

@app.post("/create-book",status_code=status.HTTP_201_CREATED )
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/update_book",status_code=status.HTTP_204_NO_CONTENT)

async def update_book(update_book:BookRequest):
    book_changed=False
    for i in range(len(BOOKS)):
        
        if BOOKS[i].id==update_book.id:
            BOOKS[i]=update_book
            book_changed=True
    if not book_changed:
        raise HTTPException(status_code=404,detail="no book updated")
    
        
@app.delete("/books/delete_book/{book_id}",status_code=status.HTTP_204_NO_CONTENT)

async def delete_book(book_id:int):
    book_changed=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book_id:
            book_changed=True
            return BOOKS.pop(i)
             
            break
    if not book_changed:
        raise HTTPException(status_code=404,detail="no book updated")    
    