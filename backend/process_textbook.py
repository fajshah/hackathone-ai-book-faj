import json
import asyncio
import random

class TextbookEmbedder:
    def __init__(self):
        self.vector_size = 1536

    async def run(self):
        textbook_data = self.read_json()
        await self.process_textbook(textbook_data)
        print("Process completed successfully!")

    def read_json(self):
        with open("./docs/textbook.json", 'r') as f:
            return json.load(f)

    def generate_embedding(self, text):
        # Generate a deterministic mock embedding based on the text content
        text_hash = hash(text) % (2**32)
        random.seed(text_hash)
        embedding = [random.uniform(-1, 1) for _ in range(self.vector_size)]
        return embedding

    async def process_textbook(self, textbook_data):
        print("Processing textbook content...")
        point_id = 1
        for chapter in textbook_data["chapters"]:
            for section in chapter["sections"]:
                embedding = self.generate_embedding(section["content"])
                print(f"Processed ID: {point_id}, Chapter: {chapter['title']}, Section: {section['title']}")
                point_id += 1
        print(f"Total sections processed: {point_id - 1}")

if __name__ == "__main__":
    embedder = TextbookEmbedder()
    asyncio.run(embedder.run())