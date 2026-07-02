from pydantic import BaseModel

from fastapi_zero.entities.user.user_public import UserPublic


class UserList(BaseModel):
    users: list[UserPublic]
