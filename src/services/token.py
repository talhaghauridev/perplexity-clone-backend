from typing import TypedDict
import jwt
from datetime import datetime, timedelta, timezone
from src.config import config
from src.utils.exceptions import ApiError


class TokenPayload(TypedDict):
    user_id: str
    email: str
    name: str
    provider: str


class TokenService:
    @staticmethod
    def generate_tokens(payload: TokenPayload) -> dict[str, str]:
        access_token = jwt.encode(
            {
                **payload,
                "exp": datetime.now(timezone.utc)
                + timedelta(seconds=config.access_token_expire),
            },
            config.access_token_secret,
            algorithm="HS256",
        )
        return {"access_token": access_token}

    @staticmethod
    def verify_access_token(token: str) -> TokenPayload:
        try:
            decoded = jwt.decode(
                token, config.access_token_secret, algorithms=["HS256"]
            )
            return TokenPayload(
                user_id=decoded["user_id"],
                email=decoded["email"],
                name=decoded["name"],
                provider=decoded["provider"],
            )
        except jwt.ExpiredSignatureError:
            raise ApiError("Token expired", status_code=401)
        except jwt.InvalidTokenError:
            raise ApiError("Invalid token", status_code=401)
