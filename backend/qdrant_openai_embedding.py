import asyncio
import json
from qdrant_client import QdrantClient
from qdrant_client.http import models
from openai import AsyncOpenAI
import hashlib

class TextbookEmbedder:
    def __init__(self, qdrant_url, api_key=None, openai_api_key=None):
        self.client = QdrantClient(url=qdrant_url, api_key=api_key)
        self.collection_name = "physical_ai"
        self.embedding_model = AsyncOpenAI(api_key=openai_api_key)

    async def create_collection(self, vector_size=1536):  # text-embedding-ada-002 has 1536 dimensions
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE)
        )
        print(f"Collection '{self.collection_name}' ready.")

    async def generate_embedding(self, text):
        if self.embedding_model.api_key:  # Check if API key is provided
            response = await self.embedding_model.embeddings.create(
                input=text,
                model="text-embedding-ada-002"  # Using ada-002 as it's more cost-effective
            )
            embedding = response.data[0].embedding
        else:
            # Generate a deterministic mock embedding if no API key is provided
            import random
            text_hash = hash(text) % (2**32)
            random.seed(text_hash)
            embedding = [random.uniform(-1, 1) for _ in range(1536)]
        return embedding

    async def insert_embeddings(self, textbook_json):
        points = []
        point_id = 1

        for chapter in textbook_json["chapters"]:
            for section in chapter["sections"]:
                vector = await self.generate_embedding(section["content"])
                points.append(
                    models.PointStruct(
                        id=point_id,
                        vector=vector,
                        payload={
                            "chapter": chapter["title"],
                            "section": section["title"],
                            "text": section["content"]
                        }
                    )
                )
                point_id += 1

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        print(f"All {len(points)} sections uploaded.")

    async def verify_upload(self):
        res = self.client.scroll(
            collection_name=self.collection_name,
            limit=5,
            with_payload=True,
            with_vectors=False
        )
        points, next_page = res
        print("\nSample points uploaded:")
        for point in points:
            print(f"ID: {point.id}, Chapter: {point.payload['chapter']}, Section: {point.payload['section']}")

    async def run(self, json_path):
        # Step 1: Load textbook JSON
        with open(json_path, "r") as f:
            textbook_json = json.load(f)

        # Step 2: Create collection
        await self.create_collection()

        # Step 3: Insert all embeddings
        await self.insert_embeddings(textbook_json)

        # Step 4: Verify upload
        await self.verify_upload()

        print("\nProcess completed successfully!")


if __name__ == "__main__":
    # Note: This can work with or without a valid OpenAI API key
    # If no API key is provided, it will use deterministic mock embeddings
    import os
    openai_api_key = os.getenv("OPENAI_API_KEY", "")

    if not openai_api_key:
        print("OpenAI API key not found. Using deterministic mock embeddings.")
        print("To use real OpenAI embeddings, set the OPENAI_API_KEY environment variable.")
    else:
        print("Using OpenAI API for embeddings.")

    embedder = TextbookEmbedder(
        qdrant_url="https://bef512c4-0759-464d-af6c-4d6e2352566c.us-east4-0.gcp.cloud.qdrant.io",
        api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.jCpXlK2HGZIHrE5j4iXF1cfFAthAmzXH-Kw-SSUhNFI",
        openai_api_key=openai_api_key
    )
    asyncio.run(embedder.run("./docs/textbook.json"))