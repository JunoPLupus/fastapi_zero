import pytest
from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND

from fastapi_zero.app import app


@pytest.fixture
def client():
    return TestClient(app)  # Arrange


def test_root_deve_retornar_ola_mundo(client):
    # Act
    response = client.get('/')
    # Assert
    assert response.status_code == HTTP_200_OK
    assert response.json() == {'message': 'Olá mundo!'}


def test_create_user_deve_retornar_user_public(client):
    # Act
    response = client.post(
        '/users/',
        json={
            'username': 'testuser',
            'email': 'test.user@gmail.com',
            'password': 'secret',
        }
    )
    # Assert
    assert response.status_code == HTTP_201_CREATED
    assert response.json() == {
        'id': 1,
        'username': 'testuser',
        'email': 'test.user@gmail.com',
    }


def test_read_users_deve_retornar_usuarios(client):
    # Act
    response = client.get('/users/')
    # Assert
    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'testuser',
                'email': 'test.user@gmail.com'
            }
        ]
    }


def test_update_user_deve_atualizar_usuario(client):
    # Act
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword'
        }
    )
    # Assert
    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        'id': 1,
        'username': 'bob',
        'email': 'bob@example.com'
    }


def test_update_user_deve_lancar_exception_quando_nao_encontrado(client):
    # Act
    response = client.put('/users/4', json={
        'username': 'bob 2',
        'email': 'bob@gmail.com',
        'password': 'newpassword'
    })
    # Assert
    assert response.status_code == HTTP_404_NOT_FOUND


def test_delete_user_deve_deletar_usuario(client):
    # Act
    response = client.delete('/users/1')
    # Assert
    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        'message': 'User deleted'
    }
