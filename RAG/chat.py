from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIG
# ============================================================

QDRANT_URL = "http://localhost:6333"

COLLECTION_NAME = "bis_knowledge"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Retrieve more documents because raw data is now indexed.
DEFAULT_LIMIT = 10


# ============================================================
# INITIALIZE
# ============================================================

print("=" * 70)
print("BIS RAG CHAT")
print("=" * 70)

print("\nConnecting to Qdrant...")

client = QdrantClient(
    url=QDRANT_URL
)

print("Connected.")

print("\nLoading embedding model...")

model = SentenceTransformer(
    EMBEDDING_MODEL
)

print("Embedding model loaded.")


# ============================================================
# SEARCH KNOWLEDGE
# ============================================================

def search_knowledge(
    query,
    limit=DEFAULT_LIMIT
):

    query_vector = model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    results = client.query_points(

        collection_name=COLLECTION_NAME,

        query=query_vector,

        limit=limit,

        with_payload=True,

    )

    return results.points


# ============================================================
# BUILD CONTEXT
# ============================================================

def build_context(results):

    context_parts = []

    for index, result in enumerate(
        results,
        start=1
    ):

        payload = result.payload or {}

        text = payload.get(
            "text",
            ""
        )

        source_type = payload.get(
            "source_type",
            ""
        )

        source_path = payload.get(
            "source_path",
            ""
        )

        product_name = payload.get(
            "product_name",
            ""
        )

        context_parts.append(

            f"""
============================================================
SOURCE {index}
============================================================

SOURCE TYPE:
{source_type}

PRODUCT:
{product_name}

SOURCE PATH:
{source_path}

RELEVANCE SCORE:
{result.score}

CONTENT:
{text}
"""
        )

    return "\n".join(
        context_parts
    )


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(results):

    print(
        "\nRetrieved knowledge:"
    )

    print(
        "-" * 70
    )

    if not results:

        print(
            "No relevant information found."
        )

        return

    for i, result in enumerate(
        results,
        start=1
    ):

        payload = (
            result.payload or {}
        )

        print(
            f"\nRESULT {i}"
        )

        print(
            f"Score       : "
            f"{result.score}"
        )

        print(
            f"Source Type : "
            f"{payload.get('source_type')}"
        )

        print(
            f"Product     : "
            f"{payload.get('product_name')}"
        )

        print(
            f"Source      : "
            f"{payload.get('source_path')}"
        )

        print(
            "\nContent:"
        )

        print(
            payload.get(
                "text",
                ""
            )
        )

        print(
            "-" * 70
        )


# ============================================================
# CHAT
# ============================================================

def main():

    print(
        "\nType 'exit' to quit."
    )

    print(
        "Type 'sources' after a query "
        "to inspect retrieved data."
    )

    last_results = []

    while True:

        question = input(
            "\nYou: "
        ).strip()

        if question.lower() == "exit":

            print(
                "\nExiting..."
            )

            break

        if not question:

            continue

        # ----------------------------------------------------
        # Show previous sources
        # ----------------------------------------------------

        if question.lower() == "sources":

            if not last_results:

                print(
                    "\nNo previous query."
                )

                continue

            display_results(
                last_results
            )

            continue

        # ----------------------------------------------------
        # Search Qdrant
        # ----------------------------------------------------

        print(
            "\nSearching BIS knowledge base..."
        )

        try:

            results = search_knowledge(
                question,
                limit=DEFAULT_LIMIT
            )

            last_results = results

        except Exception as exc:

            print(
                "\nQdrant search failed:"
            )

            print(exc)

            continue

        # ----------------------------------------------------
        # Display
        # ----------------------------------------------------

        if not results:

            print(
                "\nNo relevant information found."
            )

            continue

        # ----------------------------------------------------
        # Context
        # ----------------------------------------------------

        context = build_context(
            results
        )

        # ----------------------------------------------------
        # Current version only displays
        # retrieved context.
        #
        # The LLM generation layer should be
        # added here.
        # ----------------------------------------------------

        print(
            "\nRelevant BIS data retrieved."
        )

        print(
            f"Sources retrieved: "
            f"{len(results)}"
        )

        print(
            "\nUse 'sources' to inspect "
            "the complete retrieved data."
        )

        print(
            "\nTop relevant result:"
        )

        print(
            "-" * 70
        )

        first_payload = (
            results[0].payload or {}
        )

        print(
            first_payload.get(
                "text",
                ""
            )
        )

        print(
            "-" * 70
        )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()