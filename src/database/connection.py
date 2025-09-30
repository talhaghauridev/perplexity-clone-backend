from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .models.users import AuthProvider, VerificationType
from src.config import config

load_dotenv()


def create_database_engine(echo: bool = False):
    """Create sync engine"""
    database_url = config.database_url
    if not database_url:
        raise ValueError("DATABASE_URL not found")

    return create_engine(
        database_url, echo=echo, pool_size=5, pool_pre_ping=True, pool_recycle=3600
    )


engine = None
SessionLocal = None

db = None


def init_db():
    """Initialize database - called once at startup"""
    global engine, SessionLocal, db

    engine = create_database_engine(echo=False)
    SessionLocal = scoped_session(sessionmaker(bind=engine))

    db = SessionLocal()

    print("✅ Database initialized!")


def create_tables():
    """Create all tables"""
    from .base import Base

    AuthProvider.create(engine, checkfirst=True)
    VerificationType.create(engine, checkfirst=True)
    Base.metadata.create_all(engine)

    print("✅ Tables created!")


def close_db():
    """Close database connection"""
    global db
    if db:
        db.close()
        SessionLocal.remove()
    if engine:
        engine.dispose()
    print("🔌 Database closed!")
