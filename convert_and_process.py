import json
import os
import asyncio
import random
from pathlib import Path

class TextbookEmbedder:
    def __init__(self):
        self.vector_size = 1536

    async def run(self):
        textbook_data = self.convert_docs_to_json()
        await self.process_textbook(textbook_data)
        print("Process completed successfully!")

    def convert_docs_to_json(self):
        """Convert the markdown files in docs/ to the required JSON format"""
        docs_path = Path("frontend/text-book/docs")
        textbook_data = {"chapters": []}

        # Process intro.md if it exists
        intro_file = docs_path / "intro.md"
        if intro_file.exists():
            with open(intro_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract title from markdown (first heading)
            title = "Introduction"
            lines = content.split('\n')
            for line in lines:
                if line.startswith('# '):
                    title = line[2:].strip()
                    break

            textbook_data["chapters"].append({
                "title": title,
                "sections": [
                    {
                        "title": title,
                        "content": content
                    }
                ]
            })

        # Process chapter directories
        for chapter_dir in sorted(docs_path.iterdir()):
            if chapter_dir.is_dir() and chapter_dir.name.startswith('chapter'):
                chapter_title = chapter_dir.name.replace('chapter', 'Chapter ').replace('-', ' ')

                sections = []
                for md_file in chapter_dir.glob('*.md'):
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Extract title from markdown (first heading)
                    title = md_file.stem.replace('-', ' ').title()
                    lines = content.split('\n')
                    for line in lines:
                        if line.startswith('# '):
                            title = line[2:].strip()
                            break

                    sections.append({
                        "title": title,
                        "content": content
                    })

                if sections:  # Only add chapter if it has sections
                    textbook_data["chapters"].append({
                        "title": chapter_title,
                        "sections": sections
                    })

        # Write the JSON file
        with open("./docs/textbook.json", 'w', encoding='utf-8') as f:
            json.dump(textbook_data, f, indent=2)

        print(f"Converted textbook to JSON format with {len(textbook_data['chapters'])} chapters")
        return textbook_data

    def generate_embedding(self, text):
        # Generate a deterministic mock embedding based on the text content
        text_hash = hash(text) % (2**32)
        random.seed(text_hash)
        embedding = [random.uniform(-1, 1) for _ in range(self.vector_size)]
        return embedding

    async def process_textbook(self, textbook_data):
        print("Processing textbook content...")
        point_id = 1
        total_sections = 0

        for chapter in textbook_data["chapters"]:
            for section in chapter["sections"]:
                embedding = self.generate_embedding(section["content"])
                print(f"Processed ID: {point_id}, Chapter: {chapter['title']}, Section: {section['title'][:50]}...")
                point_id += 1
                total_sections += 1

        print(f"Total sections processed: {total_sections}")
        print("Embeddings generated successfully!")

if __name__ == "__main__":
    embedder = TextbookEmbedder()
    asyncio.run(embedder.run())