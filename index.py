import os
import json
import uuid
import hashlib
from pathlib import Path
import pypdf

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

# ============================================================
# CONFIGURATION
# ============================================================
DATA_DIR = Path(r"/home/videesh-sharma/Desktop/sih/data_collection_pipeline/data")
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "bis_knowledge"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Files and folders to explicitly ignore to prevent noise
IGNORE_KEYWORDS = [
    "regulatory_manifest", 
    "product_manual_archive", 
    "bis_act"
]

# ============================================================
# INITIALIZE
# ============================================================
print("=" * 70)
print("BIS RAG OMNI-INGESTOR (JSON + PDF + RELATIONAL ENRICHMENT)")
print("=" * 70)

# Added timeout=60 to prevent network read timeouts
client = QdrantClient(url=QDRANT_URL, timeout=60)
model = SentenceTransformer(EMBEDDING_MODEL)

try:
    VECTOR_SIZE = model.get_embedding_dimension()
except AttributeError:
    VECTOR_SIZE = model.get_sentence_embedding_dimension()

collections = [col.name for col in client.get_collections().collections]
if COLLECTION_NAME in collections:
    client.delete_collection(collection_name=COLLECTION_NAME)

client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
)
print("Connected to Qdrant. Clean collection created.")

# ============================================================
# HELPERS
# ============================================================
def make_uuid(text):
    return str(uuid.UUID(hashlib.md5(text.encode("utf-8")).hexdigest()))

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += (chunk_size - overlap)
    return chunks

def load_json(path):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def clean_rag_noise(text):
    """Removes massive arrays of unrelated IS standards from product text"""
    clean_lines = []
    for line in text.split('\n'):
        if "Standards: IS" in line and len(line) > 200:
            clean_lines.append("  [Detailed regulatory standard list omitted for clarity]")
        else:
            clean_lines.append(line)
    return "\n".join(clean_lines)

# ============================================================
# PHASE 1: BUILD THE "BRAIN"
# ============================================================
def build_standard_to_product_map(data_dir):
    """PHASE 1: Creates a dictionary linking IS Standards to Product Names."""
    mapping = {}
    rag_file = Path(data_dir) / "mapped" / "rag_records.json"
    
    if not rag_file.exists():
        print(f"Warning: {rag_file} not found. Enrichment limited.")
        return mapping
        
    records = load_json(rag_file)
    if records:
        for record in records:
            product_name = record.get("product_name", "")
            standards = record.get("standards", [])
            for std in standards:
                std_num = std.get("standard_number") if isinstance(std, dict) else str(std)
                if std_num:
                    mapping[std_num.strip()] = product_name
                    # Also map base standard (e.g. "IS 368" from "IS 368:2014")
                    mapping[std_num.split(':')[0].strip()] = product_name
                        
    print(f"Phase 1 Complete: Built map for {len(mapping)} standard variations.")
    return mapping

# ============================================================
# PHASES 2 & 3: TAG RAW DATA AND INJECT METADATA
# ============================================================
def extract_enriched_json(data, source_path, std_map):
    documents = []
    
    if isinstance(data, list):
        for item in data:
            documents.extend(extract_enriched_json(item, source_path, std_map))
        return documents

    if isinstance(data, dict):
        rec_type = None
        text_parts = []
        metadata = {"source_path": str(source_path)}
        
        # PHASE 2: Lookup Standard in the Brain
        std_num = data.get("standardNumber") or data.get("standard_number") or ""
        product_name = data.get("productName") or data.get("product_name") or ""
        
        if not product_name and std_num:
            product_name = std_map.get(str(std_num).strip(), "")
            if not product_name and ":" in str(std_num):
                product_name = std_map.get(str(std_num).split(":")[0].strip(), "")

        metadata["standard_number"] = str(std_num)
        metadata["product_name"] = str(product_name)
        
        # PHASE 3: Inject Structural Metadata into Text
        if "labName" in data or "oslCode" in data:
            rec_type = "laboratory"
            metadata["lab_state"] = str(data.get("labState", ""))
            text_parts = [
                "TYPE: LABORATORY RECORD",
                f"Related Product: {product_name}" if product_name else "",
                f"Standard: {std_num}" if std_num else "",
                f"Name: {data.get('labName', 'N/A')}",
                f"Address: {data.get('labAddress', 'N/A')}, {data.get('labCity', '')}, {data.get('labState', '')}",
                f"Contact: {data.get('contactPerson', 'N/A')} | {data.get('contactNumber', 'N/A')}"
            ]
            
        elif "licenseNo" in data or "firmName" in data:
            rec_type = "license"
            text_parts = [
                "TYPE: LICENCE RECORD",
                f"Related Product: {product_name}" if product_name else "",
                f"Standard: {std_num}" if std_num else "",
                f"Firm Name: {data.get('firmName', 'N/A')}",
                f"License Number: {data.get('licenseNo', 'N/A')}",
                f"Address: {data.get('firmAddress', 'N/A')}, {data.get('state', '')}",
                f"Validity: {data.get('validityDate', 'N/A')}"
            ]

        text_parts = [p for p in text_parts if p]
        if rec_type and len(text_parts) > 1:
            metadata["type"] = rec_type
            documents.append({"text": "\n".join(text_parts), "metadata": metadata})
        else:
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    documents.extend(extract_enriched_json(value, source_path, std_map))

    return documents

# ============================================================
# MAIN EXTRACTION ENGINE
# ============================================================
std_map = build_standard_to_product_map(DATA_DIR)

all_documents = []
stats = {"mapped_products": 0, "laboratories": 0, "licenses": 0, "pdf_chunks": 0}

print("\nExtracting Files...")
files = list(DATA_DIR.rglob("*.*"))

for path in files:
    if any(ignore in str(path).lower() for ignore in IGNORE_KEYWORDS):
        continue

    rel_path = str(path.relative_to(DATA_DIR))

    # 1. Cleaned Mapped Products
    if path.name == "rag_records.json":
        records = load_json(path)
        if records:
            for record in records:
                clean_text = clean_rag_noise(record.get("text", ""))
                all_documents.append({
                    "text": f"TYPE: PRODUCT_MAPPING\n{clean_text}",
                    "metadata": {"type": "product_mapping", "product_name": record.get("product_name"), "source_path": rel_path}
                })
                stats["mapped_products"] += 1

    # 2. Enriched Raw JSON
    elif path.suffix == ".json" and path.name != "rag_records.json":
        data = load_json(path)
        if data:
            docs = extract_enriched_json(data, rel_path, std_map)
            for d in docs:
                stats[d["metadata"]["type"]] = stats.get(d["metadata"]["type"], 0) + 1
            all_documents.extend(docs)

    # 3. PDF Parsing
    elif path.suffix == ".pdf":
        try:
            with open(path, 'rb') as f:
                reader = pypdf.PdfReader(f)
                full_text = "".join([page.extract_text() or "" for page in reader.pages]).strip()
            
            if full_text:
                chunks = chunk_text(full_text)
                for i, chunk in enumerate(chunks):
                    all_documents.append({
                        "text": f"TYPE: BIS_PDF_DOCUMENT\nSource: {path.name}\n\n{chunk}",
                        "metadata": {"type": "pdf_document", "source_path": rel_path, "chunk_index": i}
                    })
                    stats["pdf_chunks"] += 1
        except Exception:
            pass

print("\nExtraction Complete Breakdown:")
for k, v in stats.items():
    print(f" - {k.upper()}: {v}")

if not all_documents:
    raise RuntimeError("No documents were parsed successfully.")

# ============================================================
# CREATE EMBEDDINGS & UPLOAD
# ============================================================
print(f"\nCreating Embeddings for {len(all_documents)} chunks...")
texts = [doc["text"] for doc in all_documents]
embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)

print("Uploading to Qdrant (in safe batches of 50)...")
points = []
for index, (doc, emb) in enumerate(zip(all_documents, embeddings)):
    point_id = make_uuid(doc["text"] + str(index))
    points.append(PointStruct(id=point_id, vector=emb.tolist(), payload={"text": doc["text"], **doc["metadata"]}))

# Safer batch size of 50 to avoid timeout
for i in range(0, len(points), 50):
    batch = points[i:i+50]
    client.upsert(collection_name=COLLECTION_NAME, points=batch)
    print(f"Uploaded batch {i} to {i+len(batch)} / {len(points)}")

print("\n" + "=" * 70)
print(f"INDEXING COMPLETED SUCCESSFULLY. Stored {len(points)} vectors.")
print("=" * 70)