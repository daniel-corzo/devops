import uuid
from flask_jwt_extended import create_access_token
import pytest
from src.app import app
from src.models import Base, engine, session, BlockedEmail

client = app.test_client()


@pytest.fixture
def auth_token():
    """Create a JWT token for testing"""
    with app.app_context():
        return create_access_token(identity="test")


@pytest.fixture(autouse=True)
def reset_database():
    """Reset database before each test"""
    # Clear all data from tables
    try:
        # Clear the blocked_emails table
        session.query(BlockedEmail).delete()
        session.commit()
    except:
        session.rollback()
        # If tables don't exist yet, create them
        Base.metadata.create_all(engine)

    yield  # Run the test

    # No cleanup needed since we clear at the start of each test


def test_no_token_provided():
    res = client.post(
        "/blacklists",
        json={
            "app_uuid": uuid.uuid4(),
            "blocked_reason": "test",
            "email": "test@test.com",
        },
    )

    assert res.status_code == 403
    assert res.json == {"message": "Token is required"}


def test_invalid_token(auth_token):
    res = client.post(
        "/blacklists",
        json={
            "app_uuid": uuid.uuid4(),
            "blocked_reason": "test",
            "email": "test@test.com",
        },
        headers={"Authorization": "Bearer " + "invalid_token"},
    )

    assert res.status_code == 403
    assert res.json == {"message": "Invalid token"}


def test_email_not_present(auth_token):
    res = client.post(
        "/blacklists",
        json={
            "app_uuid": uuid.uuid4(),
            "blocked_reason": "test",
        },
        headers={"Authorization": "Bearer " + auth_token},
    )

    assert res.status_code == 400
    assert res.json == {"message": "Email is required"}


def test_app_uuid_not_present(auth_token):
    res = client.post(
        "/blacklists",
        json={
            "email": "test@test.com",
            "blocked_reason": "test",
        },
        headers={"Authorization": "Bearer " + auth_token},
    )

    assert res.status_code == 400
    assert res.json == {"message": "App UUID is required"}


def test_email_empty_string(auth_token):
    res = client.post(
        "/blacklists",
        json={
            "email": "",
            "app_uuid": uuid.uuid4(),
            "blocked_reason": "test",
        },
        headers={"Authorization": "Bearer " + auth_token},
    )

    assert res.status_code == 400
    assert res.json == {"message": "Email is required"}


def test_email_whitespace_only(auth_token):
    res = client.post(
        "/blacklists",
        json={
            "email": "   ",
            "app_uuid": uuid.uuid4(),
            "blocked_reason": "test",
        },
        headers={"Authorization": "Bearer " + auth_token},
    )

    assert res.status_code == 400
    assert res.json == {"message": "Email is required"}


def test_blocked_reason_not_present(auth_token):
    res = client.post(
        "/blacklists",
        json={
            "email": "test@test.com",
            "app_uuid": uuid.uuid4(),
        },
        headers={"Authorization": "Bearer " + auth_token},
    )

    assert res.status_code == 201
    assert res.json == {"message": "Email blocked successfully"}


def test_email_already_blocked(auth_token):
    res = client.post(
        "/blacklists",
        json={
            "email": "test@test.com",
            "app_uuid": uuid.uuid4(),
            "blocked_reason": "test",
        },
        headers={"Authorization": "Bearer " + auth_token},
    )

    assert res.status_code == 201
    assert res.json == {"message": "Email blocked successfully"}

    res = client.post(
        "/blacklists",
        json={
            "email": "test@test.com",
            "app_uuid": uuid.uuid4(),
            "blocked_reason": "test",
        },
        headers={"Authorization": "Bearer " + auth_token},
    )

    assert res.status_code == 400
    assert res.json == {"message": "Email already blocked"}


def test_valid_input(auth_token):
    app_uuid = uuid.uuid4()
    res = client.post(
        "/blacklists",
        json={
            "app_uuid": app_uuid,
            "blocked_reason": "test",
            "email": "test@test.com",
        },
        headers={"Authorization": "Bearer " + auth_token},
    )

    assert res.status_code == 201
    assert res.json == {"message": "Email blocked successfully"}

    blocked_emails = session.query(BlockedEmail).all()
    assert len(blocked_emails) == 1
    assert blocked_emails[0].email == "test@test.com"
    assert blocked_emails[0].app_uuid == app_uuid
    assert blocked_emails[0].blocked_reason == "test"
    assert (
        blocked_emails[0].request_ip is not None and blocked_emails[0].request_ip != ""
    )
    assert blocked_emails[0].created_at is not None


# GET TESTS
def test_get_email_not_blocked(auth_token):
    res = client.get(
        "/blacklists/test@test.com",
        headers={"Authorization": "Bearer " + auth_token},
    )

    assert res.status_code == 200
    assert res.json == {"blocked": False}


def test_get_email_blocked_with_reason(auth_token):
    res = client.post(
        "/blacklists",
        json={
            "email": "test@test.com",
            "app_uuid": uuid.uuid4(),
            "blocked_reason": "test",
        },
        headers={"Authorization": "Bearer " + auth_token},
    )

    assert res.status_code == 201
    assert res.json == {"message": "Email blocked successfully"}

    res = client.get(
        "/blacklists/test@test.com",
        headers={"Authorization": "Bearer " + auth_token},
    )

    assert res.status_code == 200
    assert res.json == {"blocked": True, "blocked_reason": "test"}


def test_get_email_blocked_without_reason(auth_token):
    res = client.post(
        "/blacklists",
        json={
            "email": "test@test.com",
            "app_uuid": uuid.uuid4(),
        },
        headers={"Authorization": "Bearer " + auth_token},
    )

    assert res.status_code == 201
    assert res.json == {"message": "Email blocked successfully"}

    res = client.get(
        "/blacklists/test@test.com",
        headers={"Authorization": "Bearer " + auth_token},
    )

    assert res.status_code == 200
    assert res.json == {"blocked": True}


# DELETE TESTS
def test_delete_all_blocked_emails(auth_token):
    res = client.post(
        "/blacklists",
        json={
            "email": "test@test.com",
            "app_uuid": uuid.uuid4(),
            "blocked_reason": "test",
        },
        headers={"Authorization": "Bearer " + auth_token},
    )
    assert res.status_code == 201

    blocked_emails = session.query(BlockedEmail).all()
    assert len(blocked_emails) == 1

    res = client.delete(
        "/blacklists",
        headers={"Authorization": "Bearer " + auth_token},
    )

    assert res.status_code == 200
    assert res.json == {"message": "All blocked emails deleted successfully"}

    blocked_emails = session.query(BlockedEmail).all()
    assert len(blocked_emails) == 0

# HEALTH TESTS
# def test_health(auth_token):
#     res = client.get(
#         "/health",
#     )

#     assert res.status_code == 200
#     assert "timestamp" in res.json
