import time
from pathlib import Path

import httpx
import jwt

from app.config import settings

GITHUB_API_URL = "https://api.github.com"


def generate_github_jwt() -> str:
    private_key = Path(settings.github_private_key_path).read_text()

    now = int(time.time())

    payload = {
        "iat": now - 60,
        "exp": now + (10 * 60),
        "iss": str(settings.github_app_id),
    }

    return jwt.encode(
        payload,
        private_key,
        algorithm="RS256",
    )


async def get_installations() -> list[dict]:
    jwt_token = generate_github_jwt()
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API_URL}/app/installations",
            headers=headers,
        )
        response.raise_for_status()
        return response.json()


async def generate_installation_token(installation_id: int) -> dict:
    jwt_token = generate_github_jwt()
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{GITHUB_API_URL}/app/installations/{installation_id}/access_tokens",
            headers=headers,
        )
        response.raise_for_status()
        return response.json()


async def get_installation_access_token(installation_id: int) -> str:
    data = await generate_installation_token(installation_id)
    return data["token"]
