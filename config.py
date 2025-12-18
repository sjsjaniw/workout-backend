from dotenv import load_dotenv
from os import getenv

load_dotenv()

DB_USER=getenv("DB_USER")
DB_PASSWORD=getenv("DB_PASSWORD")
DB_HOST=getenv("DB_HOST")
DB_PORT=getenv("DB_PORT")
DB_NAME=getenv("DB_NAME")

if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    raise ValueError("One or more required environment variables for the database are not set.")

SYNC_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
ASYNC_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"