import json
import chromadb

client = chromadb.PersistentClient(path="./bis_real_data")
collection = client.get_collection(name="bis_certifications")

# Fetch first 2 rows including documents and metadatas
results = collection.get(
    limit=2,
    include=["documents", "metadatas"]
)

for i in range(len(results["ids"])):
    row = {
        "id": results["ids"][i],
        "document": results["documents"][i],
        "metadata": results["metadatas"][i]
    }
    print(f"\n--- ROW {i + 1} ---")
    print(json.dumps(row, indent=2))