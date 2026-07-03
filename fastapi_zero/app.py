from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

from fastapi_zero.database import get_session
from fastapi_zero.entities import Message, User, UserDB, UserList, UserPublic
from fastapi_zero.models.user.user_schema import UserSchema

app = FastAPI()
database = []


@app.get('/', status_code=HTTP_200_OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo!'}


@app.get('/users/', status_code=HTTP_200_OK, response_model=UserList)
def read_users():
    return {'users': database}


@app.post('/users/', status_code=HTTP_201_CREATED, response_model=UserPublic)
def create_user(user: User, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(UserSchema).where(
            (UserSchema.username == user.username)
            | (UserSchema.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTP_409_CONFLICT, detail='Username already exists'
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTP_409_CONFLICT, detail='Email already exists'
            )

    db_user = UserSchema(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get(
    '/users/{user_id}', status_code=HTTP_200_OK, response_model=UserPublic
)
def read_one_user(user_id: int):
    # TODO: Encapsular essa busca em algum método
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail='User not found'
        )

    return database[user_id - 1]


@app.put(
    '/users/{user_id}', status_code=HTTP_200_OK, response_model=UserPublic
)
def update_user(user_id: int, user: User):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail='User not found'
        )

    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail='User not found'
        )
    del database[user_id - 1]

    return {'message': 'User deleted'}
