import json
import os
import asyncio
from qdrant_client import QdrantClient
from qdrant_client.http import models
from openai import AsyncOpenAI

class TextbookEmbedder:
    def __init__(self):
        api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.jCpXlK2HGZIHrE5j4iXF1cfFAthAmzXH-Kw-SSUhNFI"
        endpoint = "https://bef512c4-0759-464d-af6c-4d6e2352566c.us-east4-0.gcp.cloud.qdrant.io"
        openai_api_key = os.getenv("OPENAI_API_KEY", "")

        self.qdrant_client = QdrantClient(url=endpoint, api_key=api_key, prefer_grpc=False)
        self.openai_client = AsyncOpenAI(api_key=openai_api_key)
        self.collection_name = "physical_ai"
        self.vector_size = 1536

    async def run(self):
        await self.create_collection()
        textbook_data = self.read_json()
        await self.embed_and_upload(textbook_data)
        await self.verify_upload()
        print("Process completed successfully!")

    def read_json(self):
        with open("./docs/textbook.json", 'r') as f:
            return json.load(f)

    async def generate_embedding(self, text):
        response = await self.openai_client.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return response.data[0].embedding

    async def create_collection(self):
        try:
            self.qdrant_client.get_collection(self.collection_name)
        except:
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.vector_size,
                    distance=models.Distance.COSINE
                )
            )

    async def embed_and_upload(self, textbook_data):
        points = []
        point_id = 1
        for chapter in textbook_data["chapters"]:
            for section in chapter["sections"]:
                embedding = await self.generate_embedding(section["content"])
                points.append(models.PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "chapter": chapter["title"],
                        "section": section["title"],
                        "text": section["content"]
                    }
                ))
                point_id += 1
        self.qdrant_client.upsert(collection_name=self.collection_name, points=points)

    async def verify_upload(self):
        points = self.qdrant_client.scroll(
            collection_name=self.collection_name,
            limit=5,
            with_payload=True,
            with_vectors=False
        )
        for point_id, payload in zip(points[0], points[1]):
            print(f"ID: {point_id}, Chapter: {payload['chapter']}, Section: {payload['section']}")

if __name__ == "__main__":
    embedder = TextbookEmbedder()
    asyncio.run(embedder.run())