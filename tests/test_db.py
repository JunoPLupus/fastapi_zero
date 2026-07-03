from dataclasses import asdict

import pytest
from sqlalchemy import select

from fastapi_zero.models.user.user_schema import UserSchema

pytestmark = pytest.mark.integration


def test_create_user(session, mock_db_time):
    # Arrange
    with mock_db_time(model=UserSchema) as time:
        new_user = UserSchema(
            username='alice', email='teste@gmail.com', password='secret'
        )
        session.add(new_user)
        session.commit()
    # Act
    user = session.scalar(
        select(UserSchema).where(UserSchema.username == 'alice')
    )
    # Assert
    assert asdict(user) == {
        'id': 1,
        'username': new_user.username,
        'email': new_user.email,
        'password': new_user.password,
        'created_at': time,
        'updated_at': time
    }
