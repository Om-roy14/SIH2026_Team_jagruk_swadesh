from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

# Reconnect to Qdrant with a higher timeout
client = QdrantClient(url="http://localhost:6333", timeout=60)
COLLECTION_NAME = "bis_knowledge"

print(f"Resuming upload for {len(points)} points...")

# Upload in safer, smaller batches of 50
for i in range(0, len(points), 50):
    batch = points[i:i+50]
    client.upsert(collection_name=COLLECTION_NAME, points=batch)
    print(f"Uploaded batch {i} to {i+len(batch)}")

print("\n[SUCCESS] All points uploaded successfully!")