from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from ..config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
	DATABASE_URL,
	pool_size=5,
	max_overflow=10,
	pool_recycle=3600,
)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
