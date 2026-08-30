import json
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
import uuid

def fast_update():
    print("=" * 60)
    print("FAST QDRANT JSON UPDATE SCRIPT")
    print("=" * 60)

    # 1. Connect to local Qdrant instance
    client = QdrantClient(url="http://localhost:6333")
    collection_name = "bis_knowledge"

    # 2. Locate and load the newly mapped RAG records
    # Adjust path if your folder structure differs relative to the RAG folder
    rag_path_options = [
        Path("../data_collection_pipeline/data/mapped/rag_records.json"),
        Path("data/mapped/rag_records.json")
    ]
    
    rag_records_path = None
    for path in rag_path_options:
        if path.exists():
            rag_records_path = path
            break

    if not rag_records_path:
        print("Error: Could not find 'rag_records.json'. Make sure you ran python -m mapping.run first!")
        return

    with open(rag_records_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    print(f"Loaded {len(records)} records from mapping output.")

    # 3. Load embedding model
    print("Loading embedding model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # 4. Clean up old JSON records from Qdrant to prevent duplicates
    print("Removing old JSON records from Qdrant vector database...")
    try:
        client.delete(
            collection_name=collection_name,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="type",
                            match=models.MatchValue(value="json_record")
                        )
                    ]
                )
            )
        )
    except Exception as e:
        print(f"Notice during cleanup (collection might be fresh or empty): {e}")

    # 5. Embed and upload new records
    print("Embedding and uploading new records...")
    points = []
    for idx, rec in enumerate(records):
        text = rec.get("text", "")
        if not text:
            continue
        
        vector = model.encode(text).tolist()
        # Generate stable, deterministic UUID for the point
        point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"json_{idx}_{rec.get('product_name', '')}"))

        points.append(
            models.PointStruct(
                id=point_id,
                vector=vector,
                payload={
                    "type": "json_record",
                    "product_name": rec.get("product_name", ""),
                    "product_slug": rec.get("product_slug", ""),
                    "text": text
                }
            )
        )

    if points:
        client.upsert(
            collection_name=collection_name,
            points=points
        )
        print(f"\n[SUCCESS] Updated Qdrant! Inserted {len(points)} fresh JSON records into '{collection_name}'.")
    else:
        print("\n[WARNING] No valid text data found in records to upsert.")

if __name__ == "__main__":
    fast_update()