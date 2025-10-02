from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db, close_db
from .routes import router
from .config import config
from .middlewares.error_handler import error_handler_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    try:
        init_db()
        print("✅ Database connected!")

    except Exception as e:
        print(f"❌ Failed to initialize database: {str(e)}")
        raise

    yield

    try:
        close_db()
        print("👋 App stopped!")
    except Exception as e:
        print(f"Error during shutdown: {str(e)}")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Perplexity Clone API",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.allow_origins.split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.middleware("http")(error_handler_middleware)
    app.mount("/public", StaticFiles(directory="public"), name="public")

    @app.get("/favicon.ico", include_in_schema=False)
    async def favicon():
        return FileResponse("public/favicon.ico")

    app.include_router(router)

    @app.get("/")
    def read_root():
        return {"message": "Welcome to API!", "status": "running"}

    return app


app = create_app()
