from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, DeclarativeBase, declarative_base

from .config import settings

url = URL.create(
    drivername="postgresql+psycopg2",
    username=settings.db_user,
    password=settings.db_pass,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
)

# engine = create_engine(url=url) # local database connection string
engine = create_engine(url=settings.database_url) # supabase database connection string
Base: DeclarativeBase = declarative_base()
SessionLocal = sessionmaker(bind=engine)
