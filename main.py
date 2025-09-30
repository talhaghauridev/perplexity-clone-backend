from src.app import app
from src.config import config

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        port=config.port,
    )
