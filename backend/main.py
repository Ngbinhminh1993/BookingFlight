from fastapi import FastAPI
from routers import users

app = FastAPI()

app.include_router(users.router)


@app.get("/register/")
def register():
    return "user registration endpoint"


@app.get("/")
def main():
    return {"message": "Hello, World!"}
