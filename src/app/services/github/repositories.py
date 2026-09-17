import httpx


async def get_repositories(installation_token: str):
    headers = {
        "Authorization": f"Bearer {installation_token}",
        "Accept": "application/vnd.github+json",
    }

    url = "https://api.github.com/installation/repositories"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=headers,
        )

    response.raise_for_status()

    return response.json()