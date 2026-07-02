import pytest
from sqlalchemy import select

from fastapi_zero.models.user.user_schema import UserSchema

pytestmark = pytest.mark.integration


def test_create_user(session):
    # Arrange
    new_user = UserSchema(
        username='alice', password='secret', email='teste@gmail.com'
    )
    session.add(new_user)
    session.commit()
    # Act
    user = session.scalar(
        select(UserSchema).where(UserSchema.username == 'alice')
    )
    # Assert
    assert user.username == 'alice'
