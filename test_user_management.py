import pytest
from user_management import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register_success(client):
    response = client.post('/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'StrongPassword123!'
    })
    assert response.status_code == 201
    assert b'User registered successfully.' in response.data

def test_register_duplicate_username(client):
    client.post('/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'StrongPassword123!'
    })
    response = client.post('/register', json={
        'username': 'testuser',
        'email': 'test2@example.com',
        'password': 'AnotherPassword123!'
    })
    assert response.status_code == 400
    assert b'Username or email already exists' in response.data

def test_login_success(client):
    client.post('/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'StrongPassword123!'
    })
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'StrongPassword123!'
    })
    assert response.status_code == 200
    assert b'access_token' in response.data

def test_login_invalid_credentials(client):
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'WrongPassword'
    })
    assert response.status_code == 401
    assert b'Invalid username or password' in response.data
