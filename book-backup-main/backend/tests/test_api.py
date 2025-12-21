import pytest
import json
from httpx import AsyncClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app
from core.config import get_settings
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Import models after creating test engine to avoid conflicts
from core.database import Base

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
async def client_fixture(db_session):
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
    test_settings.OPENROUTER_API_KEY = "test-openrouter-key"
    test_settings.QDRANT_URL = "http://localhost:6333"
    test_settings.QDRANT_API_KEY = "test-qdrant-key"
    monkeypatch.setattr("core.config.get_settings", lambda: test_settings)

@pytest.mark.asyncio
async def test_root_endpoint(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "FastAPI backend is running!"}

@pytest.mark.asyncio
async def test_chat_endpoint(client, db_session):
    # Test the chat endpoint with mocked RAG service
    with patch("services.rag_service.rag_service.retrieve") as mock_retrieve, \
         patch("services.rag_service.rag_service.generate_embedding") as mock_generate_embedding, \
         patch("services.rag_service.rag_service.generate_rag_response") as mock_generate_rag_response:

        # Mock the RAG service methods
        mock_generate_embedding.return_value = [0.1] * 1024  # 1024-dim vector
        mock_retrieve.return_value = ["This is a relevant document chunk from the knowledge base."]
        mock_generate_rag_response.return_value = "This is the AI's response based on the retrieved documents."

        response = await client.post(
            "/api/chat",
            json={"question": "What is the capital of France?", "conversation_id": None}
        )

        assert response.status_code == 200
        data = response.json()

        # Check that response has expected structure
        assert "id" in data
        assert "title" in data
        assert "messages" in data
        assert len(data["messages"]) == 2  # User message + AI response

        # Check that user message is present
        user_msg = next((msg for msg in data["messages"] if msg["role"] == "user"), None)
        assert user_msg is not None
        assert user_msg["content"] == "What is the capital of France?"

        # Check that AI response is present
        ai_msg = next((msg for msg in data["messages"] if msg["role"] == "assistant"), None)
        assert ai_msg is not None
        assert ai_msg["content"] == "This is the AI's response based on the retrieved documents."

        # Verify mocks were called
        mock_generate_embedding.assert_called_once()
        mock_retrieve.assert_called_once()
        mock_generate_rag_response.assert_called_once()
