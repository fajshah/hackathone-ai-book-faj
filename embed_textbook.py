import json
import asyncio
import random
from qdrant_client import QdrantClient
from qdrant_client.http import models

class TextbookEmbedder:
    def __init__(self):
        self.qdrant_client = QdrantClient(url="http://localhost:6333")
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

    def generate_embedding(self, text):
        # Generate a deterministic mock embedding based on the text content
        # This ensures the same text always produces the same embedding
        text_hash = hash(text) % (2**32)
        random.seed(text_hash)
        embedding = [random.uniform(-1, 1) for _ in range(self.vector_size)]
        return embedding

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
                embedding = self.generate_embedding(section["content"])
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