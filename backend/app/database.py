from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import logging
from .core.config import settings
from .models.base import Base
from .models import user, task, notification  # Import all models

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create engine with echo=True for SQL logging
engine = create_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    try:
        # Log existing tables
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        logger.info(f"Existing tables: {existing_tables}")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Successfully created all database tables")
        
        # Log tables after creation
        inspector = inspect(engine)
        tables_after = inspector.get_table_names()
        logger.info(f"Tables after creation: {tables_after}")
        
    except SQLAlchemyError as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise

# Initialize database tables
init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()