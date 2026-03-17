#!/usr/bin/env python3
"""Test connection to the Aiven PostgreSQL database."""

import os
import sys

try:
    import psycopg2
except ImportError:
    print("psycopg2 not found. Install it with: pip install psycopg2-binary")
    sys.exit(1)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("ERROR: DATABASE_URL environment variable is not set.")
    print("Copy .env.example to .env and fill in your Aiven credentials.")
    sys.exit(1)


def test_connection():
    print(f"Connecting to: {DATABASE_URL.split('@')[1]}")  # hide credentials in output
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT version(), current_database(), current_user, now();")
        row = cur.fetchone()
        print("\n✅ Connection successful!")
        print(f"   PostgreSQL : {row[0].split(',')[0]}")
        print(f"   Database   : {row[1]}")
        print(f"   User       : {row[2]}")
        print(f"   Server time: {row[3]}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    test_connection()
