
from fastapi import FastAPI

app = FastAPI(title="Poll API")

@app.get("/")
def home():
    return {"message": "Poll API is running!"}

@app.get("/polls")
def get_polls():
    return {"polls": []}
