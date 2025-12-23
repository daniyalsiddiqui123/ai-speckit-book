import os
import httpx
from core.config import get_settings

def test_openrouter_api():
    settings = get_settings()
    api_key = settings.OPENROUTER_API_KEY
    print(f"Testing API key: {api_key[:10]}...")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Test with a simple embeddings request
    payload = {
        "model": "qwen/qwen3-embedding-8b",
        "input": "test"
    }

    try:
        with httpx.Client() as client:
            response = client.post(
                "https://openrouter.ai/api/v1/embeddings",
                headers=headers,
                json=payload,
                timeout=30.0
            )
            print(f"Response status: {response.status_code}")
            if response.status_code == 200:
                print("API key is valid!")
                data = response.json()
                print(f"Embedding dimensions: {len(data['data'][0]['embedding'])}")
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                print("The API key might be invalid or you might not have access to this model.")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_openrouter_api()