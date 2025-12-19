import pytest
from httpx import AsyncClient
from main import app
from core.config import get_settings
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.database import Base, get_db
from models.user import User
from models.conversation import Conversation
from models.message import Message

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(name="db_session")
def db_session_fixture():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(name="client")
async def client_fixture(db_session: Session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()

@pytest.fixture(autouse=True)
def mock_settings(monkeypatch):
    test_settings = get_settings()
    test_settings.SECRET_KEY = "test_secret_key"
    test_settings.ACCESS_TOKEN_EXPIRE_MINUTES = 1
    test_settings.REFRESH_TOKEN_EXPIRE_DAYS = 1
    test_settings.CLIENT_ORIGIN_URL = "http://localhost:3000"
    monkeypatch.setattr("core.config.get_settings", lambda: test_settings)

@pytest.mark.asyncio
async def test_signup_user(client: AsyncClient):
    response = await client.post(
        "/api/auth/signup",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"

@pytest.mark.asyncio
async def test_login_for_access_token(client: AsyncClient, db_session: Session):
    await client.post(
        "/api/auth/signup",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    
    response = await client.post(
        "/api/auth/login",
        data={"username": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

@pytest.mark.asyncio
async def test_chat_endpoint_global_rag(client: AsyncClient, db_session: Session):
    signup_response = await client.post(
        "/api/auth/signup",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    login_response = await client.post(
        "/api/auth/login",
        data={"username": "test@example.com", "password": "testpassword"}
    )
    access_token = login_response.json()["access_token"]

    with patch("services.rag_service.rag_service.retrieve_context") as mock_retrieve_context, \
         patch("services.rag_service.rag_service.generate_response") as mock_generate_response:
        
        mock_retrieve_context.return_value = [{"text": "context from book", "source": "ch1"}]
        
        def mock_gen_resp_side_effect(*args, **kwargs):
            yield {"type": "chunk", "content": "Hello"}
            yield {"type": "chunk", "content": " there!"}
            yield {"type": "citation", "sources": [{"source": "ch1"}]}
        mock_generate_response.side_effect = mock_gen_resp_side_effect

        response = await client.post(
            "/api/chat",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"question": "What is the capital of France?"}
        )

        assert response.status_code == 200
        content = ""
        events = response.text.split("\n")
        for event in events:
            if event.startswith("data:"):
                try:
                    data = json.loads(event[len("data:"):])
                    if data["type"] == "chunk":
                        content += data["content"]
                except json.JSONDecodeError:
                    pass # Ignore incomplete JSON lines
        
        assert "Hello there!" in content
        mock_retrieve_context.assert_called_once()
        mock_generate_response.assert_called_once()
