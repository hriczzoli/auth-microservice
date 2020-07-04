from app.api.models import User, UserInDB
from app.api.db import users, database

# Add new user to DB
async def add_user(payload: UserInDB):
    query = users.insert().values(**payload)

    return await database.execute(query = query)

# Fetch all users from DB
async def get_all_users():
    query = users.select()

    return await database.fetch_all(query = query)

# Fetch a specific user using the provided username
async def get_user_by_name(username: str):
    query = users.select(users.c.username == username)

    return await database.fetch_one(query = query)
