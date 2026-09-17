from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.repository import Repository


def parse_github_datetime(value):
    if value is None:
        return None

    return datetime.fromisoformat(value.replace("Z", "+00:00"))


async def upsert_repository(
    session: AsyncSession,
    repo_data: dict,
):
    # 1. Check karo ki repo pehle se exist karta hai ya nahi
    stmt = select(Repository).where(Repository.github_id == repo_data["id"])
    result = await session.execute(stmt)
    repository = result.scalar_one_or_none()

    # 2. Agar nahi mila, toh naya banao (Insert)
    if repository is None:
        repository = Repository(
            github_id=repo_data["id"],
            name=repo_data["name"],
            full_name=repo_data["full_name"],
            owner=repo_data["owner"]["login"],
            description=repo_data["description"],
            private=repo_data["private"],
            html_url=repo_data["html_url"],
            default_branch=repo_data["default_branch"],
            language=repo_data["language"],
            created_at=parse_github_datetime(repo_data["created_at"]),
            updated_at=parse_github_datetime(repo_data["updated_at"]),
            pushed_at=parse_github_datetime(repo_data["pushed_at"]),
        )
        session.add(repository)
    else:
        # 3. Agar mil gaya, toh update karo (Update)
        repository.name = repo_data["name"]
        repository.full_name = repo_data["full_name"]
        repository.owner = repo_data["owner"]["login"]
        repository.description = repo_data["description"]
        repository.private = repo_data["private"]
        repository.html_url = repo_data["html_url"]
        repository.default_branch = repo_data["default_branch"]
        repository.language = repo_data["language"]
        repository.updated_at = parse_github_datetime(repo_data["updated_at"])
        repository.pushed_at = parse_github_datetime(repo_data["pushed_at"])

    # 4. Save to DB
    await session.commit()
    return repository