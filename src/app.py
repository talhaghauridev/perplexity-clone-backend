from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db, create_tables, close_db
from .routes import router
from .config import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    create_tables()
    print("✅ Database connected!")

    yield

    close_db()
    print("👋 App stopped!")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Perplexity Clone API",
        lifespan=lifespan,
        debug=True,
    )
    print(config.allow_origins.split(","))

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.allow_origins.split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
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
