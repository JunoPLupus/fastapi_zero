import pytest
from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND

from fastapi_zero.app import app
from tests.mothers.user_mother import UserMockFactory, UserPublicMockFactory


# region fixtures
@pytest.fixture(scope='class')
def client():
    return TestClient(app)  # Arrange


@pytest.fixture
def user_mock():
    return UserMockFactory.create()  # Arrange


@pytest.fixture
def user_public_mock():
    return UserPublicMockFactory.create()  # Arrange


# endregion


class TestRoot:
    def test_deve_retornar_ola_mundo(self, client):
        # Act
        response = client.get('/')
        # Assert
        assert response.status_code == HTTP_200_OK
        assert response.json() == {'message': 'Olá mundo!'}


class TestCreateUser:
    def test_deve_cadastrar_usuario(self, client, user_mock, user_public_mock):
        # Act
        response = client.post('/users/', json=user_mock.model_dump())
        # Assert
        assert response.status_code == HTTP_201_CREATED
        assert response.json() == user_public_mock.model_dump()


class TestReadUsers:
    def test_deve_retornar_usuarios(self, client, user_mock, user_public_mock):
        # Arrange
        client.post('/users/', json=user_mock.model_dump())
        user_public_mock_2 = UserPublicMockFactory.create(id=2)
        # Act
        response = client.get('/users/')
        # Assert
        assert response.status_code == HTTP_200_OK
        assert response.json() == {
            'users': [
                user_public_mock.model_dump(),
                user_public_mock_2.model_dump(),
            ]
        }


class TestReadOneUser:
    def test_deve_retornar_usuario(self, client, user_mock, user_public_mock):
        # Arrange
        client.post('/users/', json=user_mock.model_dump())
        # Act
        response = client.get('/users/1')
        # Assert
        assert response.status_code == HTTP_200_OK
        assert response.json() == user_public_mock.model_dump()

    def test_deve_lancar_exception_quando_nao_encontrado(self, client):
        # Act
        response = client.get('/users/4')
        # Assert
        assert response.status_code == HTTP_404_NOT_FOUND


class TestUpdateUser:
    def test_deve_atualizar_usuario(self, client, user_mock, user_public_mock):
        # Arrange
        client.post('/users/', json=user_mock.model_dump())
        # Act
        response = client.put('/users/1', json=user_mock.model_dump())
        # Assert
        assert response.status_code == HTTP_200_OK
        assert response.json() == user_public_mock.model_dump()

    def test_deve_lancar_exception_quando_nao_encontrado(
        self, client, user_mock
    ):
        # Act
        response = client.put('/users/404', json=user_mock.model_dump())
        # Assert
        assert response.status_code == HTTP_404_NOT_FOUND


class TestDeleteUser:
    def test_deve_deletar_usuario(self, client, user_mock):
        # Arrange
        client.post('/users/', json=user_mock.model_dump())
        # Act
        response = client.delete('/users/1')
        # Assert
        assert response.status_code == HTTP_200_OK
        assert response.json() == {'message': 'User deleted'}

    def test_deve_lancar_exception_quando_nao_encontrado(self, client):
        # Act
        response = client.delete('/users/404')
        # Assert
        assert response.status_code == HTTP_404_NOT_FOUND
