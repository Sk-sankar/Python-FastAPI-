from fastapi import FastAPI
from pydantic import BaseModel

class NewArticle(BaseModel):
    Title:str
    discription:str
    author:str
app = FastAPI(title="Demo")
@app.get("/")
def hello():
    return {"status":200}

@app.get("/v1/articles")
def get_articles():
    return {"data":[]}

@app.get("/v1/articles/{id}")
def get_article_by_id(id:"str"):
    print(id)
    return{"data":{"id":id}}

@app.post("/v1/articles")
def create_article(new_article:NewArticle):
    print(new_article)
    return {"status":201}
    
    
@app.put("/v1/articles/{id}")
def modify_data(updated:NewArticle):
    print(updated)
    return{"status":201}

@app.delete("/v1/articles/{id}")
def delete_data(deleted:NewArticle):
    print(deleted)
    return {"status":200}
    
    
    


    


if __name__ == "__main__":
    
    hello()
    print (__name__)
    



