from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK

from fastapi_zero.app import app


def test_root_deve_retornar_ola_mundo():
    # Arrange
    client = TestClient(app)
    # Act
    response = client.get('/')
    # Assert
    assert response.status_code == HTTP_200_OK
    assert response.json() == {'message': 'Olá mundo!'}
