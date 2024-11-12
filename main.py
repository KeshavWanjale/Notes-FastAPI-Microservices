from fastapi import FastAPI
from fastapi import APIRouter
from user_service.routes import user_routes


app = FastAPI()

app.include_router(user_routes, prefix="/api/users", tags=["users"])

@app.get("/")
def root():
    return {"message": "Hello World"}