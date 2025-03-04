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
import os
from datetime import datetime

# Get database connection information from environment variables
DATABASE_URL = os.getenv("DATABASE_DSN", "")

# Create a database engine
engine = create_engine(DATABASE_URL)
# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()


# Define the Twitter model
class Twitter(Base):
    __tablename__ = "twitter"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


# Check and update database tables
def check_and_update_tables():
    inspector = inspect(engine)
    models = [Twitter]

    for model in models:
        table_name = model.__tablename__
        if not inspector.has_table(table_name):
            # Create the table if it doesn't exist
            print(f"Table {table_name} does not exist. Creating...")
            model.__table__.create(bind=engine)


# Provide a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
