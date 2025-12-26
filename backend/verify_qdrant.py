from qdrant_client import QdrantClient
import json

client = QdrantClient(url="https://bef512c4-0759-464d-af6c-4d6e2352566c.us-east4-0.gcp.cloud.qdrant.io", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.jCpXlK2HGZIHrE5j4iXF1cfFAthAmzXH-Kw-SSUhNFI")
res = client.scroll(collection_name="physical_ai", limit=15)

# Print the first few records with readable content
points, next_page = res
print(f"Retrieved {len(points)} points from the collection")
print(f"Next page: {next_page}")

for i, point in enumerate(points[:5]):  # Only print first 5 for readability
    print(f"\nPoint {i+1}:")
    print(f"  ID: {point.id}")
    print(f"  Chapter: {point.payload.get('chapter', 'N/A')}")
    print(f"  Section: {point.payload.get('section', 'N/A')}")
    print(f"  Text preview: {point.payload.get('text', '')[:100]}...")