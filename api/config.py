import os

APP_ENV = os.getenv("APP_ENV", "development")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PSWD = os.getenv("DB_PSWD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "dates_facts_db")
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@db/dates_facts_db"
).replace("postgres://", "postgresql://", 1)
