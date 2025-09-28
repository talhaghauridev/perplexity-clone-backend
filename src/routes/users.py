# src/routes/users.py
from fastapi import APIRouter

users = APIRouter(prefix="/users", tags=["users"])


@users.get("/{user_id}")
def read_user(user_id: int):
    return {"user_id": user_id}
