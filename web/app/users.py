from users import Client
from users.api.default import auth_by_password as api_auth_by_password, users as api_users
from users.models.auth_by_password_request import AuthByPasswordRequest
from users.models.filters import Filters
from typing import Optional, List

from .api import raise_on_errors
from .schemas import Profile

# return token or None
async def auth_by_password(client: Client, username: str, password: str) -> Optional[str]:
    response = await api_auth_by_password.asyncio_detailed(client=client, json_body=AuthByPasswordRequest(password=password, username=username))
    raise_on_errors(response)
    if not response.parsed.ok:
        return None
    return response.parsed.token

async def find(client: Client, ids: Optional[List[int]]) -> List[Profile]:
    response = await api_users.asyncio_detailed(client=client, json_body=Filters(ids=ids))
    raise_on_errors(response)
    items = []
    for rprofile in response.parsed.items:
        items.append(Profile(uid=rprofile.uid, name=rprofile.name))
    return items 
