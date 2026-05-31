#!/usr/bin/env python3
"""
Test database connection and pgvector availability.
Run this after starting the Docker container.
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL not set in .env file")
    sys.exit(1)

print(f"Testing connection to: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else DATABASE_URL}")

try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker

    print("✓ SQLAlchemy imported")

    # Create engine
    engine = create_engine(DATABASE_URL, echo=False)
    print("✓ Engine created")

    # Test connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print(f"✓ Connected to PostgreSQL: {version.split(',')[0]}")

    # Test pgvector extension
    with engine.connect() as conn:
        result = conn.execute(text("SELECT installed_version FROM pg_available_extensions WHERE name = 'vector';"))
        version = result.fetchone()
        if version and version[0]:
            print(f"✓ pgvector extension installed (v{version[0]})")
        else:
            print("⚠ pgvector extension not enabled — run: CREATE EXTENSION vector;")

    # Test creating tables
    from models import Base
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created successfully")

    # Verify tables
    with engine.connect() as conn:
        result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';"))
        tables = [row[0] for row in result.fetchall()]
        print(f"✓ Tables in database: {', '.join(tables)}")

    print("\n✅ Database setup complete and working!")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
