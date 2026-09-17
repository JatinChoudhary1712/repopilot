from langchain_core.tools import tool
from sqlalchemy import text

from app.db.session import AsyncSessionLocal


@tool
async def execute_sql_query(query: str) -> list[dict] | str:
    """
    Execute a read-only SQL SELECT query on the PostgreSQL database.
    Use this tool whenever you need to query repository data, such as:
    - Exact counting: SELECT COUNT(*) FROM repositories;
    - Filtering by language: SELECT name, language FROM repositories WHERE language = 'Python';
    - Finding private/public: SELECT name FROM repositories WHERE private = true;
    - Inactive repositories: SELECT name, pushed_at FROM repositories WHERE pushed_at < NOW() - INTERVAL '6 months';
    - Language aggregation: SELECT language, COUNT(*) FROM repositories GROUP BY language;

    Only SELECT queries are allowed.
    """
    clean_query = query.strip()

    # 1. Security Check: Sirf SELECT query allow karo
    if not clean_query.lower().startswith("select"):
        return "Error: Security violation. Only read-only SELECT queries are allowed."

    # 2. Database par execute karo
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text(clean_query))
            rows = result.mappings().all()
            return [dict(row) for row in rows]
    except Exception as e:
        # Error return karo taaki LLM use padh kar query fix kar sake
        return f"SQL Execution Error: {str(e)}"