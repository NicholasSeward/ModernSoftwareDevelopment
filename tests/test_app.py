import pytest
from TDDDemo.app import app, db, User
from flask import Flask


@pytest.fixture
def test_client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    # db.init_app(app)

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


def test_get_users_empty_database(test_client):
    response = test_client.get('/users')
    assert response.status_code == 200
    assert response.get_json() == []

def test_get_users_with_data(test_client):
    with test_client.application.app_context():
        user1 = User(name="Test User 1", email="test1@example.com")
        user2 = User(name="Test User 2", email="test2@example.com")
        db.session.add_all([user1, user2])
        db.session.commit()

    response = test_client.get('/users')
    assert response.status_code == 200
    assert response.get_json() == [
        {"id": 1, "name": "Test User 1", "email": "test1@example.com"},
        {"id": 2, "name": "Test User 2", "email": "test2@example.com"},
    ]


def test_get_users_data_structure(test_client):
    with test_client.application.app_context():
        user = User(name="Test User", email="test@example.com")
        db.session.add(user)
        db.session.commit()

    response = test_client.get('/users')
    assert response.status_code == 200
    result = response.get_json()
    assert isinstance(result, list)
    assert len(result) == 1
    assert all(key in result[0] for key in ["id", "name", "email"])


def test_add_user(test_client):
    response = test_client.get('/add_user?name=Test User&email=test@example.com')
    assert response.status_code == 200
    user = User.query.order_by(User.id.desc()).first()
    assert user is not None
    assert user.name == "Test User"
    assert user.email == "test@example.com"
    
    #assert response.get_json() == {"message": "User added successfully"}


def test_add_user_bad_email(test_client):
    response = test_client.get('/add_user?name=Test User&email=testexample.com')
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid email format"}
