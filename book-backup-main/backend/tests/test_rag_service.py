import pytest
from unittest.mock import MagicMock, patch
import asyncio
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.rag_service import RAGService
from core.config import get_settings

# Mock settings for testing
@pytest.fixture(autouse=True)
def mock_settings(monkeypatch):
    test_settings = get_settings()
    test_settings.OPENROUTER_API_KEY = "test_openrouter_key"
    test_settings.QDRANT_URL = "http://localhost:6333"
    test_settings.QDRANT_API_KEY = "test_qdrant_key"
    monkeypatch.setattr("core.config.get_settings", lambda: test_settings)

@pytest.fixture
def rag_service_instance():
    with patch('services.rag_service.QdrantClient') as MockQdrantClient:
        # Configure mock QdrantClient
        mock_client_instance = MagicMock()
        MockQdrantClient.return_value = mock_client_instance
        service = RAGService()
        yield service, mock_client_instance

def test_retrieve(rag_service_instance):
    service, mock_client = rag_service_instance

    # Mock collection info and search results
    mock_collection_info = MagicMock()
    mock_collection_info.config.params.vectors_config.size = 1024
    mock_client.get_collection.return_value = mock_collection_info

    mock_hits = [
        MagicMock(payload={"text": "chunk 1", "source": "doc1.md"}),
        MagicMock(payload={"text": "chunk 2", "source": "doc2.md"})
    ]
    mock_client.search.return_value = mock_hits

    # Test retrieve method
    embedding = [0.1] * 1024
    results = service.retrieve(embedding)

    assert len(results) == 2
    assert results[0] == "chunk 1"
    assert results[1] == "chunk 2"
    mock_client.search.assert_called_once_with(
        collection_name=service.collection_name,
        query_vector=embedding,
        limit=5,
    )

@pytest.mark.asyncio
async def test_generate_embedding(rag_service_instance):
    service, _ = rag_service_instance

    with patch('services.rag_service.httpx.AsyncClient') as MockAsyncClient:
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": [{"embedding": [0.1, 0.2, 0.3]}]}
        mock_response.raise_for_status.return_value = None
        mock_client.post.return_value.__aenter__.return_value = mock_response
        MockAsyncClient.return_value = mock_client

        embedding = await service.generate_embedding("test query")

        assert embedding == [0.1, 0.2, 0.3]
        mock_client.post.assert_called_once()

@pytest.mark.asyncio
async def test_generate_rag_response(rag_service_instance):
    service, _ = rag_service_instance

    with patch('services.rag_service.httpx.AsyncClient') as MockAsyncClient:
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "This is the AI response"}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_client.post.return_value.__aenter__.return_value = mock_response
        MockAsyncClient.return_value = mock_client

        retrieved_docs = ["This is a relevant document chunk."]
        response = await service.generate_rag_response("What is it?", retrieved_docs)

        assert response == "This is the AI response"
        mock_client.post.assert_called_once()
