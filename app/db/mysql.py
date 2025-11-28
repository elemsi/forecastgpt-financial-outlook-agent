from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.utils.config import settings
from app.utils.logger import get_logger

log = get_logger("mysql")

# Build the normal MySQL URL first
DATABASE_URL = (
    f"mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}"
    f"@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DB}"
)

# We will try MySQL first; if it is not reachable (e.g. during an interview demo
# where MySQL is not running), we silently fall back to a local SQLite DB so
# the FastAPI app keeps working without noisy stack traces.
def _create_engine_with_fallback():
    try:
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        # light-weight connectivity check
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        log.info("Connected to MySQL successfully.")
        return engine
    except Exception as e:  # pragma: no cover - defensive for local demos
        log.warning(
            f"MySQL not available or connection failed ({e}). "
            "Falling back to local SQLite database for logging."
        )
        sqlite_url = "sqlite:///./forecastgpt_fallback.db"
        return create_engine(sqlite_url, echo=False, future=True)

engine = _create_engine_with_fallback()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
