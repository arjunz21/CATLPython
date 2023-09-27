from fastapi import Depends, FastAPI, HTTPException, status, Form
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    username: str
    password: str


class Data(BaseModel):
    fname: str
    lname: str


@app.get("/test/{item_id}")
async def test(item_id: str, query: int = 1):
    return {"hello": item_id, "query": query}


@app.post("/create")
async def create(data: Data):
    return {"data": data}


@app.post("/submit/", response_model=User)
async def submit(nm: str = Form(...), pwd: str = Form(...)):
    return User(username=nm, password=pwd)
