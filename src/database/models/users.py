from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, DateTime, Boolean, Text, ForeignKey, Index
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.constants import (
    AVAILABLE_AUTH_PROVIDERS,
    AVAILABLE_VERIFICATIONS,
    AuthProviderType,
)
from src.utils.mixins import TimestampMixin
from ..base import Base, UUIDPk, UUIDFk

AuthProvider = ENUM(*AVAILABLE_AUTH_PROVIDERS, name="auth_provider", create_type=False)

VerificationType = ENUM(
    *AVAILABLE_VERIFICATIONS, name="verification_type", create_type=False
)


class User(Base, TimestampMixin):
    __tablename__ = "users"
    id: Mapped[UUIDPk]
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(60))
    profile_picture: Mapped[Optional[str]] = mapped_column(Text)
    provider: Mapped[str] = mapped_column(AuthProvider, default=AuthProviderType.CUSTOM)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    verifications: Mapped[List["Verification"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Verification(Base, TimestampMixin):
    __tablename__ = "verifications"

    id: Mapped[UUIDPk]
    user_id: Mapped[UUIDFk] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    type: Mapped[str] = mapped_column(VerificationType)
    token: Mapped[str] = mapped_column(String(255))
    expires_at: Mapped[datetime] = mapped_column(DateTime)

    user: Mapped["User"] = relationship(back_populates="verifications")

    __table_args__ = (Index("user_type_idx", "user_id", "type"),)
