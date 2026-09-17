import asyncio

from app.db.session import AsyncSessionLocal
from app.repositories.repository import create_repository
from app.services.github.auth import (
    get_installations,
    generate_installation_token,
)
from app.services.github.repositories import get_repositories


async def main():
    # Get GitHub installation
    installations = await get_installations()

    installation_id = installations[0]["id"]

    # Get installation token
    token_data = await generate_installation_token(
        installation_id
    )

    token = token_data["token"]

    # Get repositories
    data = await get_repositories(token)

    # Get all repositories
    repositories = data["repositories"]

    print(f"Found {len(repositories)} repositories")

    # Save repositories to database
    for repo_data in repositories:
        async with AsyncSessionLocal() as session:
            repository = await create_repository(
                session,
                repo_data,
            )

            print(
                "Saved repository:",
                repository.name,
                repository.github_id,
            )


if __name__ == "__main__":
    asyncio.run(main())