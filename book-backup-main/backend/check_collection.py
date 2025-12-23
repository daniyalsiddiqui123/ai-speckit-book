#!/usr/bin/env python3
"""
Script to check if the Qdrant collection exists and has data
"""
import os
from qdrant_client import QdrantClient
from core.config import get_settings

def check_collection():
    settings = get_settings()

    client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
    )

    collection_name = "docusaurus_book"  # This matches the ingestion script

    print(f"Checking collection: {collection_name}")
    print(f"QDRANT_URL: {settings.QDRANT_URL}")
    print(f"EMBEDDING_MODEL: {settings.EMBEDDING_MODEL}")

    try:
        # List all collections
        collections = client.get_collections()
        print(f"Available collections: {[col.name for col in collections.collections]}")

        # Check our specific collection
        collection_info = client.get_collection(collection_name)
        print(f"Collection '{collection_name}' exists!")
        print(f"Points count: {collection_info.points_count}")
        print(f"Config: {collection_info.config}")

        if collection_info.points_count > 0:
            # Sample some points to see what's in there
            points = client.scroll(
                collection_name=collection_name,
                limit=2,
                with_payload=True,
                with_vectors=False
            )

            print("\nSample points:")
            for i, (point, _) in enumerate(points[0]):
                payload = point.payload
                print(f"Point {i+1}:")
                print(f"  ID: {point.id}")
                print(f"  Text preview: {payload.get('text', '')[:100]}...")
                print(f"  Source: {payload.get('source', 'N/A')}")
                print(f"  Heading: {payload.get('heading', 'N/A')}")
                print()
        else:
            print("Collection is empty!")

    except Exception as e:
        print(f"Error accessing collection: {e}")
        print("The collection may not exist yet - you may need to run the ingestion script first.")

if __name__ == "__main__":
    check_collection()