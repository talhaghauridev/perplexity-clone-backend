from typing import Optional
from ..database import db, User


class UserService:
    @staticmethod
    def create_user(name: str, email: str, password: str) -> User:
        user = User(name=name, email=email, password=password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_by_id(user_id: str) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_all(skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def update_verification(user_id: str, is_verified: bool = True) -> bool:
        user = UserService.get_by_id(user_id)
        if user:
            user.is_verified = is_verified
            db.commit()
            return True
        return False
