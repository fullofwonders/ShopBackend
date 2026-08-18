import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

db_user = os.getenv("db_user", "postgres")
password = os.getenv("password", "admin")
db_host = os.getenv("db_host", "localhost")
port = os.getenv("port", "5432")
db_name = os.getenv("db_name", "shop_db")

secret_key = os.getenv("secret_key", "fallback_secret")
Algorithm = os.getenv("Algorithm", "HS256")

DATABASE_URL = f"postgresql+asyncpg://{db_user}:{password}@{db_host}:{port}/{db_name}"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session_maker() as session:
        yield session
