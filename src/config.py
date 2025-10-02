from pydantic_settings import BaseSettings


class Config(BaseSettings):
    database_url: str
    debug: bool = False
    port: int = 8000
    allow_origins: str = "*"
    access_token_secret: str
    access_token_expire: int

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


config = Config()
