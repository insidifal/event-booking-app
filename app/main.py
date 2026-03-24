from model import dbUsers, User
users = dbUsers() # empty db initialized

from fastapi import FastAPI
app = FastAPI()

@app.get("/users")
async def fetch_user():
    userlist = users.list()
    return { "results": userlist }

@app.post("/newuser/{username}")
async def create_new_user(user: User):
    newuser = users.new_user(user)
    return { "user": newuser }

