import os
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str
    test_database_url: Optional[str] = "postgresql://postgres:postgres@db/dates_facts_test_db"
    port: str = 8000
