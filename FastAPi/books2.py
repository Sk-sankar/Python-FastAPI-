from fastapi import FastAPI,Body

app=FastAPI()

class Book:
    id:int
    title:str
    author:str
    description:str
    rating:int
    
    def __init__(self,id,title,author,description,rating):
        self.id=id  
        self.title=title
        self.author=author
        self.description=description
        self.rating=rating
        


BOOKS=[
    Book(1,'Title One','Author One','Description One',5),
    Book(2,'Title Two','Author Two','Description Two',4),
    Book(3,'Title Three','Author Three','Description Three',3),
    Book(4,'Title Four','Author Four','Description Four',2),
    Book(5,'Title Five','Author Five','Description Four',1),
]

@app.get("/books")

async def read_all_books():
    return BOOKS

@app.post("/create_book")

async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    return new_book