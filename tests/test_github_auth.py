import asyncio
import pytest

from app.services.github.auth import get_installations


@pytest.mark.anyio
async def test_get_installations():
    installations = await get_installations()
    assert isinstance(installations, list)
    assert len(installations) > 0
    assert "account" in installations[0]


async def main():
    installations = await get_installations()
    print("Fetched GitHub Installations:")
    for inst in installations:
        account_name = inst.get("account", {}).get("login")
        inst_id = inst.get("id")
        print(f"- Account: {account_name} (ID: {inst_id})")


if __name__ == "__main__":
    asyncio.run(main())
