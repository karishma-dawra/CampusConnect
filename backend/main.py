from fastapi import FastAPI
from database import create_table

app = FastAPI()

create_table()

@app.get("/")
def home():
    return {"message": "CampusConnect backend is running"}
