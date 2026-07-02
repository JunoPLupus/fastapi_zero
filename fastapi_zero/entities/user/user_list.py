from pydantic import BaseModel

from fastapi_zero.entities import UserPublic


class UserList(BaseModel):
    users: list[UserPublic]
