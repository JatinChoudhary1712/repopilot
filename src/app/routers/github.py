from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.repository import upsert_repository
from app.services.github.auth import (
    generate_installation_token,
    get_installations,
)
from app.services.github.repositories import get_repositories

router = APIRouter(prefix="/github", tags=["github"])


@router.post("/sync")
async def sync_repositories(session: AsyncSession = Depends(get_db)):
    # Step 1: GitHub installation lo
    installations = await get_installations()
    first_installation = installations[0]
    installation_id = first_installation["id"]

    # Step 2: GitHub se temporary access token lo
    token_data = await generate_installation_token(installation_id)
    token = token_data["token"]

    # Step 3: GitHub API se repositories fetch karo
    data = await get_repositories(token)
    repositories = data["repositories"]

    # Step 4: Har repository ko database mein save ya update karo
    for repo_data in repositories:
        await upsert_repository(session, repo_data)

    # Step 5: User ko output return karo
    return {
        "status": "success",
        "total_synced": len(repositories),
    }