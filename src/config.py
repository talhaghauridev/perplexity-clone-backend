from pydantic_settings import BaseSettings


class Config(BaseSettings):
    database_url: str
    debug: bool = False
    port: int = 8000
    allow_origins: str = "*"

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


config = Config()
