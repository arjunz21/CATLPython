from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "OK"}

client = TestClient(app)

def test_home():
    res = client.get("/")

    assert res.status_code == 200
    assert res.json() == {"message": "OK"}