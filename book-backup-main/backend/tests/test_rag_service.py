import pytest
from unittest.mock import MagicMock, patch

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
    with patch('qdrant_client.QdrantClient') as MockQdrantClient, \
         patch('openai.OpenAI') as MockOpenAI:
        # Configure mocks if needed
        # MockQdrantClient.return_value = MagicMock()
        # MockOpenAI.return_value = MagicMock()
        service = RAGService()
        yield service, MockQdrantClient, MockOpenAI

def test_get_embedding(rag_service_instance):
    service, _, MockOpenAI = rag_service_instance
    mock_embedding_response = MagicMock()
    mock_embedding_response.data = [MagicMock(embedding=[0.1, 0.2, 0.3])]
    MockOpenAI.return_value.embeddings.create.return_value = mock_embedding_response
    
    embedding = service.get_embedding("test query")
    assert embedding == [0.1, 0.2, 0.3]
    MockOpenAI.return_value.embeddings.create.assert_called_once_with(
        model=service.qwen_embedding_model,
        input="test query"
    )

def test_retrieve_context(rag_service_instance):
    service, MockQdrantClient, _ = rag_service_instance
    mock_search_result = [
        MagicMock(payload={"text": "chunk 1", "source": "s1"}),
        MagicMock(payload={"text": "chunk 2", "source": "s2"})
    ]
    MockQdrantClient.return_value.search.return_value = mock_search_result
    
    context = service.retrieve_context("test query")
    assert len(context) == 2
    assert context[0]["text"] == "chunk 1"
    MockQdrantClient.return_value.search.assert_called_once() # More specific asserts can be added

def test_generate_response(rag_service_instance):
    service, _, MockOpenAI = rag_service_instance
    mock_stream_chunk1 = MagicMock()
    mock_stream_chunk1.choices = [MagicMock(delta=MagicMock(content="Hello"))]
    mock_stream_chunk2 = MagicMock()
    mock_stream_chunk2.choices = [MagicMock(delta=MagicMock(content=" World"))]

    MockOpenAI.return_value.chat.completions.create.return_value = iter([mock_stream_chunk1, mock_stream_chunk2])

    context_chunks = [{"text": "context here", "source": "test_source"}]
    response_generator = service.generate_response("What is it?", context_chunks)
    
    chunks = []
    citations = []
    for item in response_generator:
        if item["type"] == "chunk":
            chunks.append(item["content"])
        elif item["type"] == "citation":
            citations = item["sources"]
    
    assert "".join(chunks) == "Hello World"
    assert len(citations) == 1
    assert citations[0]["source"] == "test_source"
    
    MockOpenAI.return_value.chat.completions.create.assert_called_once() # More specific asserts can be added
