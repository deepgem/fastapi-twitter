from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    inspect,
    ForeignKey,
)
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
import os
from datetime import datetime

# Retrieve database connection string from environment variables, default to empty string if not set
DATABASE_URL = os.getenv("DATABASE_DSN", "")

# Create a base class for declarative SQLAlchemy models
Base = declarative_base()


def get_engine():
    """
    Attempt to create a database engine and session factory.
    Try to connect to the database. If successful, return the engine and session factory; otherwise, return None.
    """
    try:
        # Create a database engine using the provided connection string
        engine = create_engine(DATABASE_URL)
        # Create a session factory bound to the engine
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        # Test the database connection
        with engine.connect() as connection:
            print("Successfully connected to PostgreSQL!")
            return engine, SessionLocal
    except OperationalError as e:
        print(
            f"Failed to connect to PostgreSQL. DATABASE_URL: {DATABASE_URL}, Error: {e}"
        )
        return None, None
    except Exception as e:
        print(f"An error occurred: {e}, DATABASE_URL: {DATABASE_URL}")
        return None, None
    return None, None


# Define the Twitter model representing a table in the database
class Twitter(Base):
    __tablename__ = "twitter"
    # Primary key column with indexing
    id = Column(Integer, primary_key=True, index=True)
    # Text column to store the content
    content = Column(Text)
    # Column to store the creation time, defaulting to the current UTC time
    created_at = Column(DateTime, default=datetime.utcnow)


def check_and_update_tables():
    """
    Check if the required database tables exist.
    If any table is missing, create it in the database.
    """
    engine, SessionLocal = get_engine()
    if not engine:
        return
    # Create an inspector to check table existence
    inspector = inspect(engine)
    # List of models to check tables for
    models = [Twitter]

    for model in models:
        table_name = model.__tablename__
        if not inspector.has_table(table_name):
            # Create the table if it doesn't exist
            print(f"Table {table_name} not found. Creating...")
            model.__table__.create(bind=engine)


def get_db():
    """
    Obtain a database session.
    If the database connection is successful, return a session; otherwise, return None.
    """
    engine, SessionLocal = get_engine()
    if not engine:
        return None
    try:
        # Create a new database session
        db = SessionLocal()
        return db
    except Exception as e:
        print(f"An error occurred while getting the database session: {e}")
        return None
