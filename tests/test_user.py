from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'no.such.user@example.com'})
    assert response.status_code == 404
    assert isinstance(response.json(), dict)

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    duplicate = {
        'name': 'Duplicate',
        'email': users[0]['email']
    }
    response = client.post("/api/v1/user", json=duplicate)
    assert response.status_code in (400, 409)
    assert isinstance(response.json(), dict)

def test_delete_user():
    '''Удаление пользователя'''
    target_email = users[1]['email']
    response = client.delete("/api/v1/user", params={'email': target_email})
    assert response.status_code in (200, 204)

    get_resp = client.get("/api/v1/user", params={'email': target_email})
    assert get_resp.status_code == 404