from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import OperationalError
import time
import logging
from src.config import config

load_dotenv()
logger = logging.getLogger(__name__)


def create_database_engine(echo: bool = False):
    """Create database engine"""
    database_url = config.database_url
    if not database_url:
        raise ValueError("DATABASE_URL not found")

    return create_engine(
        database_url, echo=echo, pool_size=5, pool_pre_ping=True, pool_recycle=3600
    )


engine = None
SessionLocal = None
db = None


def init_db(max_retries: int = 5, retry_delay: int = 2):
    """Initialize database with retry logic"""
    global engine, SessionLocal, db

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Connecting to database (attempt {attempt}/{max_retries})...")

            engine = create_database_engine(echo=config.debug)

            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            SessionLocal = scoped_session(sessionmaker(bind=engine))
            db = SessionLocal()

            logger.info("✅ Database initialized!")
            return

        except OperationalError as e:
            logger.warning(
                f"Connection failed (attempt {attempt}/{max_retries}): {str(e)}"
            )

            if attempt == max_retries:
                logger.error("❌ Failed to connect to database")
                raise

            wait_time = retry_delay * attempt
            logger.info(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)


def close_db():
    """Close database connections"""
    global db, engine

    try:
        if db:
            db.close()
            SessionLocal.remove()

        if engine:
            engine.dispose()

        logger.info("🔌 Database closed!")

    except Exception as e:
        logger.error(f"Error closing database: {str(e)}")
