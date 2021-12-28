from pydantic import BaseModel
from typing import Optional, List

class AuthResponse(BaseModel):
    ok: bool
    token: Optional[str]

class AuthByPasswordRequest(BaseModel):
    username: str
    password: str

class Profile(BaseModel):
    uid: int
    name: str

class Profiles(BaseModel):
    items: List[Profile]

class Filters(BaseModel):
    ids: Optional[List[int]]
