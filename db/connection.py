"""PostgreSQL connection helper using psycopg2 and DATABASE_URL from .env."""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    """Return a new psycopg2 connection to the Aiven PostgreSQL database."""
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is not set. Copy .env.example to .env and fill in your credentials."
        )
    return psycopg2.connect(DATABASE_URL)
