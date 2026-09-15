# session.py is responsible for connecting RepoPilot to PostgreSQL and managing database sessions.
# It will handle:

# How to connect to the database
# Creating/reusing connections
# Creating database sessions for queries and transactions
# Closing sessions properly

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings


engine = create_async_engine(
    settings.database_url,
    echo=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)