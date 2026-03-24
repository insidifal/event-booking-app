from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str | None = None
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    age: int | None = None

class dbUsers():
    users: list[User]

    def __init__(self):
        self.users = {}

    def list(self):
        return list(self.users)

    def new_user(self, user: User):
        self.users.update( { user.username: user } )
        return user.username

    def get_user(self, username: str):
        return self.users.get(username)

    def test_user(self):
        return "Test"
