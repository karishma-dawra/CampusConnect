from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def home():
    return {"message": "CampusConnect backend is running"}