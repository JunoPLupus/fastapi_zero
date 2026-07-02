from fastapi_zero.entities.user.user import User


class UserDB(User):
    id: int
