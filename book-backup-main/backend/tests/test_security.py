import pytest
from datetime import timedelta
from jose import jwt

from core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)
from core.config import get_settings

# Mock settings for testing
@pytest.fixture(autouse=True)
def mock_settings(monkeypatch):
    test_settings = get_settings()
    test_settings.SECRET_KEY = "test_secret_key"
    test_settings.ACCESS_TOKEN_EXPIRE_MINUTES = 1
    test_settings.REFRESH_TOKEN_EXPIRE_DAYS = 1
    monkeypatch.setattr("core.config.get_settings", lambda: test_settings)

def test_password_hashing():
    password = "testpassword"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password)
    assert not verify_password("wrongpassword", hashed_password)

def test_create_access_token():
    user_email = "test@example.com"
    token = create_access_token(data={"sub": user_email})
    assert isinstance(token, str)

    decoded_token_data = decode_token(token)
    assert decoded_token_data is not None
    assert decoded_token_data.email == user_email

def test_create_refresh_token():
    user_email = "test@example.com"
    token = create_refresh_token(data={"sub": user_email})
    assert isinstance(token, str)

def test_decode_token_valid():
    user_email = "test@example.com"
    access_token = create_access_token(data={"sub": user_email}, expires_delta=timedelta(minutes=5))
    token_data = decode_token(access_token)
    assert token_data is not None
    assert token_data.email == user_email

def test_decode_token_expired():
    user_email = "test@example.com"
    expired_token = create_access_token(data={"sub": user_email}, expires_delta=timedelta(minutes=-1))
    token_data = decode_token(expired_token)
    assert token_data is None

def test_decode_token_invalid_signature():
    token = jwt.encode({"sub": "test@example.com", "exp": datetime.utcnow() + timedelta(minutes=5)}, "wrong_secret", algorithm=ALGORITHM)
    token_data = decode_token(token)
    assert token_data is None

def test_decode_token_no_sub():
    token = create_access_token(data={"foo": "bar"}, expires_delta=timedelta(minutes=5))
    token_data = decode_token(token)
    assert token_data is None
