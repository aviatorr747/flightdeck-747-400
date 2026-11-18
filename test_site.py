from app.models import User
from app import db

def register(client, username="testpilot", email="pilot@example.com",
             password="long-test-password-123"):
    return client.post("/auth/register", data={
        "username": username,
        "email": email,
        "password": password,
        "confirm_password": password,
    }, follow_redirects=True)

def test_homepage_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"THE QUEEN" in response.data
    assert b"Boeing 747-400" in response.data

def test_facts_api_returns_items(client):
    response = client.get("/api/facts")
    assert response.status_code == 200
    assert len(response.get_json()) >= 5

def test_register_creates_hashed_password(app, client):
    response = register(client)
    assert response.status_code == 200
    with app.app_context():
        user = User.query.filter_by(username="testpilot").first()
        assert user is not None
        assert user.password_hash != "long-test-password-123"
        assert user.check_password("long-test-password-123")

def test_duplicate_registration_is_rejected(client):
    register(client)
    response = register(client, username="testpilot", email="other@example.com")
    assert b"already registered" in response.data

def test_login_and_protected_explorer(client):
    register(client)
    response = client.get("/explore")
    assert response.status_code == 200
    assert b"Welcome aboard" in response.data

def test_wrong_password_does_not_login(client):
    register(client)
    client.post("/auth/logout", follow_redirects=True)
    response = client.post("/auth/login", data={
        "identity": "testpilot",
        "password": "incorrect-password",
    }, follow_redirects=True)
    assert b"not recognised" in response.data
    assert b"Sign in" in response.data

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.get_json() == {"status": "ok"}
