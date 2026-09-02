from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "bis_knowledge"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

client = QdrantClient(url=QDRANT_URL)
model = SentenceTransformer(EMBEDDING_MODEL)

query = "how many pressure cooker testing laboratory are there in india"

query_vector = model.encode(
    query,
    normalize_embeddings=True
).tolist()

results = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,
    limit=20,
    with_payload=True,
)

print("\n========== RAW QDRANT RESULTS ==========\n")

for i, point in enumerate(results.points):
    print(f"\n========== RESULT {i + 1} ==========")
    print("ID:", point.id)
    print("SCORE:", point.score)

    payload = point.payload or {}

    print("PAYLOAD KEYS:", list(payload.keys()))

    for key, value in payload.items():
        text = str(value)

        if len(text) > 1000:
            text = text[:1000] + "..."

        print(f"\n{key}:")
        print(text)