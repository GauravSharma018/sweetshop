from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# CHANGE THESE IF YOUR MYSQL USER/PASSWORD ARE DIFFERENT
DB_USER = "root"
DB_PASSWORD = "9459888291"
DB_HOST = "localhost"
DB_NAME = "sweetshop"

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    echo=True  # logs SQL queries (good for learning/debugging)
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
