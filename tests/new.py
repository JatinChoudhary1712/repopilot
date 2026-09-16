import asyncio

from app.services.github.auth import (
    generate_installation_token,
    get_installations,
)


async def main():
    installations = await get_installations()

    if not installations:
        print("No installations found.")
        return

    installation_id = installations[0]["id"]

    token_data = await generate_installation_token(installation_id)

    print("Token generated successfully")
    print("Expires at:", token_data["expires_at"])


if __name__ == "__main__":
    asyncio.run(main())