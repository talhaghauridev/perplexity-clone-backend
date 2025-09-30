from fastapi import APIRouter, HTTPException
from src.services import UserService

users = APIRouter(prefix="/users", tags=["users"])


@users.post("/")
def create_user(name: str, email: str, password: str):
    """Super clean - no db parameter anywhere!"""
    existing = UserService.get_by_email(email)
    if existing:
        raise HTTPException(400, "User exists")

    user = UserService.create_user(name, email, password)
    return {"id": str(user.id), "name": user.name, "email": user.email}


@users.get("/{user_id}")
def get_user(user_id: str):
    """Clean - no db parameter!"""
    user = UserService.get_by_id(user_id)
    if not user:
        raise HTTPException(404, "Not found")
    return {"id": str(user.id), "name": user.name, "email": user.email}


@users.get("/")
def get_users(skip: int = 0, limit: int = 100):
    """Clean - no db anywhere!"""
    users = UserService.get_all(skip, limit)
    return [{"id": str(u.id), "name": u.name, "email": u.email} for u in users]


@users.patch("/{user_id}/verify")
def verify_user(user_id: str):
    """Super clean!"""
    success = UserService.update_verification(user_id)
    if not success:
        raise HTTPException(404, "Not found")
    return {"message": "Verified!"}
