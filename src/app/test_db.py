import asyncio
import pytest
from sqlalchemy import text

from app.db.session import engine


@pytest.mark.anyio
async def test_connection():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        assert result.scalar() == 1


if __name__ == "__main__":
    asyncio.run(test_connection())