import httpx
from typing import Any

async def get_eventbrite_user(api_key: str) -> dict[str, Any]:
    if not isinstance(api_key, str):
        raise TypeError("API key is not string")

    headers = { "Authorization": f"Bearer {api_key}" }
    url = "https://www.eventbriteapi.com/v3/users/me/"

    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

