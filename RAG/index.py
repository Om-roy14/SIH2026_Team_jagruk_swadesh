import json
import hashlib
from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)

from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

# Root data directory
DATA_DIR = Path(
    r"D:\SIH2026\data_collection_pipeline\data"
)

# Mapped data
MAPPED_DIR = DATA_DIR / "mapped"

# Raw scraped data
RAW_DIR = DATA_DIR / "raw"

# Qdrant Docker container
QDRANT_URL = "http://localhost:6333"

COLLECTION_NAME = "bis_knowledge"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# ============================================================
# INITIALIZE
# ============================================================

print("=" * 70)
print("BIS RAG INDEXER")
print("=" * 70)

print("\nData root:")
print(DATA_DIR)

print("\nMapped data:")
print(MAPPED_DIR)

print("\nRaw data:")
print(RAW_DIR)


# ============================================================
# CONNECT TO QDRANT
# ============================================================

print("\nConnecting to Qdrant...")

client = QdrantClient(
    url=QDRANT_URL
)

print("Connected.")


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

print("\nLoading embedding model...")

model = SentenceTransformer(
    EMBEDDING_MODEL
)

# New method
try:
    VECTOR_SIZE = model.get_embedding_dimension()
except AttributeError:
    VECTOR_SIZE = model.get_sentence_embedding_dimension()

print(
    f"Embedding model : {EMBEDDING_MODEL}"
)

print(
    f"Vector dimension: {VECTOR_SIZE}"
)


# ============================================================
# CREATE / RECREATE COLLECTION
# ============================================================

collections = [
    collection.name
    for collection in client.get_collections().collections
]

if COLLECTION_NAME in collections:

    print(
        f"\nDeleting existing collection: "
        f"{COLLECTION_NAME}"
    )

    client.delete_collection(
        collection_name=COLLECTION_NAME
    )


print(
    f"\nCreating collection: "
    f"{COLLECTION_NAME}"
)

client.create_collection(

    collection_name=COLLECTION_NAME,

    vectors_config=VectorParams(
        size=VECTOR_SIZE,
        distance=Distance.COSINE,
    ),
)


# ============================================================
# HELPERS
# ============================================================

def load_json(path):
    """
    Safely load JSON.
    """

    try:

        with path.open(
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except UnicodeDecodeError:

        try:

            with path.open(
                "r",
                encoding="utf-8-sig"
            ) as f:

                return json.load(f)

        except Exception as exc:

            print(
                f"[WARNING] Could not decode JSON: "
                f"{path}"
            )

            print(
                f"          {exc}"
            )

            return None

    except json.JSONDecodeError as exc:

        print(
            f"[WARNING] Invalid JSON: {path}"
        )

        print(
            f"          {exc}"
        )

        return None

    except OSError as exc:

        print(
            f"[WARNING] Could not read: {path}"
        )

        print(
            f"          {exc}"
        )

        return None


def make_id(text):

    digest = hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()

    return digest[:32]


def stringify(value, level=0):

    """
    Convert arbitrary JSON data into
    readable text for embedding.
    """

    if value is None:

        return ""

    if isinstance(value, str):

        return value.strip()

    if isinstance(value, bool):

        return str(value)

    if isinstance(value, (int, float)):

        return str(value)

    if isinstance(value, list):

        parts = []

        for item in value:

            text = stringify(
                item,
                level + 1
            )

            if text:

                parts.append(text)

        return "\n".join(parts)

    if isinstance(value, dict):

        parts = []

        for key, val in value.items():

            text = stringify(
                val,
                level + 1
            )

            if text:

                parts.append(
                    f"{key}: {text}"
                )

        return "\n".join(parts)

    return str(value)


# ============================================================
# RAG RECORD CONVERSION
# ============================================================

def record_to_text(record):

    """
    Convert one mapped RAG record
    into searchable text.
    """

    text_parts = []

    # --------------------------------------------------------
    # PRODUCT
    # --------------------------------------------------------

    product_name = record.get(
        "product_name",
        ""
    )

    product_id = record.get(
        "product_id",
        ""
    )

    text_parts.append(
        "PRODUCT\n"
        f"Product Name: {product_name}\n"
        f"Product ID: {product_id}"
    )

    # --------------------------------------------------------
    # PRODUCT DETAILS
    # --------------------------------------------------------

    product = record.get(
        "product",
        {}
    )

    if product:

        text_parts.append(
            "PRODUCT DETAILS\n"
            + stringify(product)
        )

    # --------------------------------------------------------
    # STANDARDS
    # --------------------------------------------------------

    standards = record.get(
        "standards",
        []
    )

    if standards:

        text_parts.append(
            "STANDARDS\n"
            + stringify(standards)
        )

    # --------------------------------------------------------
    # QCO
    # --------------------------------------------------------

    qcos = record.get(
        "qcos",
        []
    )

    if qcos:

        text_parts.append(
            "QUALITY CONTROL ORDERS (QCO)\n"
            + stringify(qcos)
        )

    # --------------------------------------------------------
    # REGULATIONS
    # --------------------------------------------------------

    regulations = record.get(
        "regulations",
        []
    )

    if regulations:

        text_parts.append(
            "REGULATIONS\n"
            + stringify(regulations)
        )

    # --------------------------------------------------------
    # RELATIONSHIPS
    # --------------------------------------------------------

    relationships = record.get(
        "relationships",
        []
    )

    if relationships:

        text_parts.append(
            "RELATIONSHIPS\n"
            + stringify(relationships)
        )

    return "\n\n".join(
        text_parts
    )


# ============================================================
# LOAD MAPPED RAG DATA
# ============================================================

def load_mapped_records():

    documents = []

    rag_file = (
        MAPPED_DIR /
        "rag_records.json"
    )

    if not rag_file.exists():

        print(
            f"[WARNING] Missing mapped RAG file:\n"
            f"{rag_file}"
        )

        return documents

    print(
        "\nLoading mapped RAG records:"
    )

    print(rag_file)

    records = load_json(
        rag_file
    )

    if not isinstance(
        records,
        list
    ):

        print(
            "[WARNING] rag_records.json "
            "does not contain a list."
        )

        return documents

    print(
        f"Mapped RAG records found: "
        f"{len(records)}"
    )

    for index, record in enumerate(
        records
    ):

        if not isinstance(
            record,
            dict
        ):
            continue

        text = record_to_text(
            record
        )

        if not text.strip():
            continue

        documents.append({

            "text": text,

            "source_type":
                "mapped_rag",

            "source_path":
                str(rag_file),

            "product_name":
                record.get(
                    "product_name"
                ),

            "product_id":
                record.get(
                    "product_id"
                ),

            "record_index":
                index,

        })

    return documents


# ============================================================
# LOAD ALL RAW JSON DATA
# ============================================================

def load_raw_json_documents():

    """
    Load EVERY JSON file under data/raw.

    This is important because the mapped RAG records
    do not contain all scraped information.

    For example:

        license data
        laboratory data
        regulatory data
        API responses
        BIS records
        etc.
    """

    documents = []

    if not RAW_DIR.exists():

        print(
            f"[WARNING] Raw directory does not exist:\n"
            f"{RAW_DIR}"
        )

        return documents

    json_files = sorted(
        RAW_DIR.rglob("*.json")
    )

    print(
        "\nRaw JSON files discovered: "
        f"{len(json_files)}"
    )

    for path in json_files:

        data = load_json(
            path
        )

        if data is None:
            continue

        text = stringify(
            data
        )

        if not text.strip():
            continue

        # Add filename/path context.
        document_text = (
            "BIS RAW SCRAPED DATA\n\n"
            f"FILE: {path.name}\n"
            f"PATH: {path}\n\n"
            f"{text}"
        )

        documents.append({

            "text":
                document_text,

            "source_type":
                "raw_json",

            "source_path":
                str(path),

            "product_name":
                None,

            "product_id":
                None,

            "record_index":
                None,

        })

        print(
            f"  Loaded: {path}"
        )

    return documents


# ============================================================
# LOAD ALL DATA
# ============================================================

print("\n" + "=" * 70)
print("LOADING KNOWLEDGE")
print("=" * 70)


mapped_documents = (
    load_mapped_records()
)

raw_documents = (
    load_raw_json_documents()
)


documents = (
    mapped_documents +
    raw_documents
)


print(
    "\nMapped documents : "
    f"{len(mapped_documents)}"
)

print(
    "Raw JSON documents: "
    f"{len(raw_documents)}"
)

print(
    "TOTAL DOCUMENTS   : "
    f"{len(documents)}"
)


if not documents:

    raise RuntimeError(
        "No documents were found to index."
    )


# ============================================================
# PREPARE TEXT
# ============================================================

texts = [
    document["text"]
    for document in documents
]


# ============================================================
# CREATE EMBEDDINGS
# ============================================================

print(
    "\n" + "=" * 70
)

print(
    "CREATING EMBEDDINGS"
)

print(
    "=" * 70
)

embeddings = model.encode(

    texts,

    normalize_embeddings=True,

    show_progress_bar=True,
)


# ============================================================
# BUILD QDRANT POINTS
# ============================================================

points = []


for index, (
    document,
    embedding
) in enumerate(
    zip(
        documents,
        embeddings
    )
):

    point_id = make_id(

        f"{document['source_path']}"
        f"_{document['record_index']}"
        f"_{index}"

    )

    points.append(

        PointStruct(

            id=point_id,

            vector=embedding.tolist(),

            payload={

                "text":
                    document["text"],

                "source_type":
                    document[
                        "source_type"
                    ],

                "source_path":
                    document[
                        "source_path"
                    ],

                "product_name":
                    document[
                        "product_name"
                    ],

                "product_id":
                    document[
                        "product_id"
                    ],

                "record_index":
                    document[
                        "record_index"
                    ],

            }

        )
    )


# ============================================================
# UPLOAD TO QDRANT
# ============================================================

print(
    "\n" + "=" * 70
)

print(
    f"UPLOADING {len(points)} "
    f"POINTS TO QDRANT"
)

print(
    "=" * 70
)


client.upsert(

    collection_name=
        COLLECTION_NAME,

    points=points,

    wait=True,
)


# ============================================================
# VERIFY
# ============================================================

collection_info = client.get_collection(
    COLLECTION_NAME
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print(
    "\n" + "=" * 70
)

print(
    "INDEXING COMPLETED"
)

print(
    "=" * 70
)

print(
    f"Collection : "
    f"{COLLECTION_NAME}"
)

print(
    f"Mapped docs: "
    f"{len(mapped_documents)}"
)

print(
    f"Raw docs   : "
    f"{len(raw_documents)}"
)

print(
    f"Total docs : "
    f"{len(points)}"
)

print(
    f"Vector size: "
    f"{VECTOR_SIZE}"
)

print(
    f"Qdrant     : "
    f"{QDRANT_URL}"
)

print(
    "=" * 70
)