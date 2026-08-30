from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import re

# ============================================================
# CONFIGURATION
# ============================================================

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "bis_knowledge"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Number of candidates retrieved from Qdrant
RETRIEVAL_LIMIT = 8

# Maximum number of useful results sent back
MAX_RESULTS = 4

# Maximum characters allowed in the final RAG context
# ~12,000 characters is roughly 3,000 tokens depending on text.
MAX_CONTEXT_CHARS = 12000

# Maximum size of a single retrieved document
MAX_DOCUMENT_CHARS = 5000


# ============================================================
# ALLOWED PRODUCTS
# ============================================================

ALLOWED_PRODUCTS = [
    "domestic_gas_stove_and_built_in_hob_for_use_with_lpg_specification_(sixth_revision_)",
    "domestic_pressure_cooker_-_specification_(seventh_revision)",
    "electric_immersion_water_heaters_-_specification_(fifth_revision)",
    "electric_iron_-_specification_(fourth_revision)",
    "ordinary_portland_cement_-_specification_(sixth_revision)",
    "packaged_drinking_water_other_than_packaged_natural_mineral_water_specification_third_revision",
    "protective_helmets_for_motorcycle_riders_-_specification_(fourth_revision)",
    "refrigerator_or_combined_refrigerator_and_water-pack_freezer_intermittent_mains_powered_-_compression_cycle_-_general_requirements_and_test_methods",
    "room_air_conditioners_specification_part_1_unitary_air_conditioners_fourth_revision",
    "safety_glass_-_specification_part_1_architectural,_building_and_general_uses_(fourth_revision)",
    "safety_of_electric_toys",
    "textiles_polyamide_tyre_cord_fabric_for_automotive_tyres_specification_(first_revision)",
    "unplasticized_pvc_pipes_for_potable_water_supplies_-_specification_(fourth_revision)",
    "valve_for_compressed_gas_cylinders_excluding_liquefied_petroleum_gas_(lpg)_cylinders_-_specification_(fourth_revision)",
]


# ============================================================
# INITIALIZATION
# ============================================================

print("Connecting to Qdrant...")

client = QdrantClient(
    url=QDRANT_URL
)

print("Loading model...")

model = SentenceTransformer(
    EMBEDDING_MODEL
)

print("Ready!\n")


# ============================================================
# NORMALIZATION
# ============================================================

def normalize(text):
    """
    Normalize text for comparison.
    """

    if not text:
        return ""

    text = str(text).lower()

    text = re.sub(
        r"[^a-z0-9]+",
        " ",
        text
    )

    return " ".join(
        text.split()
    )


# ============================================================
# PRODUCT DETECTION
# ============================================================

PRODUCT_ALIASES = {

    "helmet": "protective_helmets_for_motorcycle_riders_-_specification_(fourth_revision)",

    "motorcycle helmet":
        "protective_helmets_for_motorcycle_riders_-_specification_(fourth_revision)",

    "bike helmet":
        "protective_helmets_for_motorcycle_riders_-_specification_(fourth_revision)",

    "pressure cooker":
        "domestic_pressure_cooker_-_specification_(seventh_revision)",

    "immersion rod":
        "electric_immersion_water_heaters_-_specification_(fifth_revision)",

    "immersion heater":
        "electric_immersion_water_heaters_-_specification_(fifth_revision)",

    "immersion water heater":
        "electric_immersion_water_heaters_-_specification_(fifth_revision)",

    "electric iron":
        "electric_iron_-_specification_(fourth_revision)",

    "iron":
        "electric_iron_-_specification_(fourth_revision)",

    "gas stove":
        "domestic_gas_stove_and_built_in_hob_for_use_with_lpg_specification_(sixth_revision)",

    "gas hob":
        "domestic_gas_stove_and_built_in_hob_for_use_with_lpg_specification_(sixth_revision)",

    "cement":
        "ordinary_portland_cement_-_specification_(sixth_revision)",

    "drinking water":
        "packaged_drinking_water_other_than_packaged_natural_mineral_water_specification_third_revision",

    "packaged drinking water":
        "packaged_drinking_water_other_than_packaged_natural_mineral_water_specification_third_revision",

    "helmet":
        "protective_helmets_for_motorcycle_riders_-_specification_(fourth_revision)",

    "refrigerator":
        "refrigerator_or_combined_refrigerator_and_water-pack_freezer_intermittent_mains_powered_-_compression_cycle_-_general_requirements_and_test_methods",

    "air conditioner":
        "room_air_conditioners_specification_part_1_unitary_air_conditioners_fourth_revision",

    "air conditioner":
        "room_air_conditioners_specification_part_1_unitary_air_conditioners_fourth_revision",

    "ac":
        "room_air_conditioners_specification_part_1_unitary_air_conditioners_fourth_revision",

    "safety glass":
        "safety_glass_-_specification_part_1_architectural,_building_and_general_uses_(fourth_revision)",

    "electric toy":
        "safety_of_electric_toys",

    "tyre cord":
        "textiles_polyamide_tyre_cord_fabric_for_automotive_tyres_specification_(first_revision)",

    "pvc pipe":
        "unplasticized_pvc_pipes_for_potable_water_supplies_-_specification_(fourth_revision)",

    "pvc pipes":
        "unplasticized_pvc_pipes_for_potable_water_supplies_-_specification_(fourth_revision)",

    "gas cylinder valve":
        "valve_for_compressed_gas_cylinders_excluding_liquefied_petroleum_gas_(lpg)_cylinders_-_specification_(fourth_revision)",
}


def detect_product(query):
    """
    Detect one of the supported products from the user's query.
    """

    q = normalize(query)

    # Check common aliases first
    for alias, product in PRODUCT_ALIASES.items():

        if normalize(alias) in q:

            return product

    # Check full product names
    for product in ALLOWED_PRODUCTS:

        readable = normalize(product)

        if readable in q:

            return product

    return None


# ============================================================
# NOISE DETECTION
# ============================================================

NOISY_SOURCES = [
    "regulatory_manifest",
    "product_manual_archive",
]

NOISY_TERMS = [
    "endpoint:",
    "responses:",
    "pagination",
    "api response",
]


def is_noisy_document(payload):
    """
    Detect large archive/index documents that commonly
    contain hundreds of unrelated standards.
    """

    text = payload.get(
        "text",
        ""
    )

    source = str(
        payload.get(
            "source_path",
            ""
        )
    ).lower()

    text_lower = text.lower()

    # Archive / manifest documents
    for source_name in NOISY_SOURCES:

        if source_name in source:

            return True

    # Huge documents containing massive IS-number lists
    is_numbers = re.findall(
        r"\bIS\s*\d+(?::\d{4})?\b",
        text,
        flags=re.IGNORECASE
    )

    if len(is_numbers) > 80:

        return True

    # API noise
    for term in NOISY_TERMS:

        if term in text_lower:

            return True

    return False


# ============================================================
# PRODUCT RELEVANCE
# ============================================================

def product_matches(payload, product):
    """
    Check whether a Qdrant payload belongs to the
    resolved product.
    """

    if not product:
        return True

    product_name = normalize(
        payload.get(
            "product_name",
            ""
        )
    )

    payload_text = normalize(
        payload.get(
            "text",
            ""
        )
    )

    target = normalize(product)

    # Exact product metadata match
    if product_name == target:

        return True

    # Product name appears in the actual document
    if target in payload_text:

        return True

    # Some records may use shortened names
    product_words = target.split()

    matching_words = sum(
        1
        for word in product_words
        if len(word) > 4 and word in payload_text
    )

    return matching_words >= 3


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):
    """
    Remove excessive whitespace while preserving
    useful BIS information.
    """

    if not text:
        return ""

    text = str(text)

    # Remove excessive blank lines
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    # Remove excessive spaces
    text = re.sub(
        r"[ \t]{2,}",
        " ",
        text
    )

    return text.strip()


# ============================================================
# DOCUMENT COMPACTION
# ============================================================

def compact_document(text):
    """
    Keep the most useful portion of a large document.

    Preference is given to product / standard / testing /
    licence / laboratory / QCO information.
    """

    text = clean_text(text)

    if len(text) <= MAX_DOCUMENT_CHARS:

        return text

    lines = text.splitlines()

    priority_keywords = [
        "product",
        "standard",
        "testing",
        "test",
        "laboratory",
        "licence",
        "license",
        "qco",
        "regulation",
        "certification",
        "requirement",
        "scope",
        "amendment",
        "corrigendum",
    ]

    important = []
    other = []

    for line in lines:

        lower = line.lower()

        if any(
            keyword in lower
            for keyword in priority_keywords
        ):

            important.append(line)

        else:

            other.append(line)

    selected = []

    for line in important:

        selected.append(line)

        if len(
            "\n".join(selected)
        ) >= MAX_DOCUMENT_CHARS:

            break

    if len(
        "\n".join(selected)
    ) < MAX_DOCUMENT_CHARS:

        for line in other:

            selected.append(line)

            if len(
                "\n".join(selected)
            ) >= MAX_DOCUMENT_CHARS:

                break

    result = "\n".join(
        selected
    )

    return result[
        :MAX_DOCUMENT_CHARS
    ]


# ============================================================
# SEARCH
# ============================================================

def search_knowledge(
    query,
    limit=RETRIEVAL_LIMIT
):
    """
    Search Qdrant and return compact,
    relevant evidence only.
    """

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

    points = results.points

    # --------------------------------------------------------
    # Detect product
    # --------------------------------------------------------

    detected_product = detect_product(
        query
    )

    # --------------------------------------------------------
    # Filter and rank
    # --------------------------------------------------------

    filtered = []

    for point in points:

        payload = point.payload or {}

        text = payload.get(
            "text",
            ""
        )

        if not text.strip():

            continue

        # Remove giant archive documents
        if is_noisy_document(payload):

            continue

        # If a product is detected, prefer
        # records belonging to that product
        if detected_product:

            if not product_matches(
                payload,
                detected_product
            ):

                continue

        filtered.append(point)

    # --------------------------------------------------------
    # Deduplicate
    # --------------------------------------------------------

    unique = []

    seen = set()

    for point in filtered:

        payload = point.payload or {}

        text = clean_text(
            payload.get(
                "text",
                ""
            )
        )

        # Hash first part of text
        fingerprint = normalize(
            text[:1000]
        )

        if fingerprint in seen:

            continue

        seen.add(
            fingerprint
        )

        unique.append(point)

    # --------------------------------------------------------
    # Compact documents
    # --------------------------------------------------------

    final_results = []

    total_chars = 0

    for point in unique:

        payload = point.payload or {}

        original_text = payload.get(
            "text",
            ""
        )

        compacted = compact_document(
            original_text
        )

        if not compacted:

            continue

        # Respect total context limit
        remaining = (
            MAX_CONTEXT_CHARS
            - total_chars
        )

        if remaining <= 0:

            break

        compacted = compacted[
            :remaining
        ]

        # Copy payload so original Qdrant
        # result is not modified
        new_payload = dict(
            payload
        )

        new_payload["text"] = compacted

        point.payload = new_payload

        final_results.append(
            point
        )

        total_chars += len(
            compacted
        )

        if len(final_results) >= MAX_RESULTS:

            break

    return final_results


# ============================================================
# BUILD LLM CONTEXT
# ============================================================

def build_context(
    results
):
    """
    Build a compact context string for the LLM.
    """

    if not results:

        return ""

    sections = []

    for i, result in enumerate(
        results,
        start=1
    ):

        payload = result.payload or {}

        product = payload.get(
            "product_name",
            ""
        )

        standard = payload.get(
            "standard_number",
            ""
        )

        text = payload.get(
            "text",
            ""
        )

        section = (
            f"[EVIDENCE {i}]\n"
            f"Product: {product}\n"
            f"Standard: {standard}\n"
            f"{text}"
        )

        sections.append(
            section
        )

    context = "\n\n---\n\n".join(
        sections
    )

    return context[
        :MAX_CONTEXT_CHARS
    ]


# ============================================================
# DISPLAY
# ============================================================

def main():

    print("=" * 70)

    print(
        "BIS COMPLIANCE RAG - SMART SEARCH"
    )

    print("=" * 70)

    print(
        "Type 'exit' to quit.\n"
    )

    while True:

        question = input(
            "\nYou: "
        ).strip()

        if question.lower() == "exit":

            break

        if not question:

            continue

        detected_product = detect_product(
            question
        )

        print(
            "\nDetected product:",
            detected_product
            if detected_product
            else "Not identified"
        )

        results = search_knowledge(
            question
        )

        print(
            "\n" + "-" * 70
        )

        print(
            "RELEVANT RETRIEVED EVIDENCE:"
        )

        print(
            "-" * 70
        )

        if not results:

            print(
                "No relevant BIS evidence found."
            )

            continue

        context = build_context(
            results
        )

        print(
            f"\nContext size: "
            f"{len(context):,} characters"
        )

        print(
            f"Results used: "
            f"{len(results)}"
        )

        for i, result in enumerate(
            results,
            start=1
        ):

            payload = result.payload or {}

            print(
                f"\n[EVIDENCE {i}]"
            )

            print(
                f"Score: "
                f"{result.score:.4f}"
            )

            print(
                f"Product: "
                f"{payload.get('product_name', 'N/A')}"
            )

            print(
                f"Standard: "
                f"{payload.get('standard_number', 'N/A')}"
            )

            print(
                f"Source: "
                f"{payload.get('source_path', 'N/A')}"
            )

            print(
                "-" * 30
            )

            print(
                payload.get(
                    "text",
                    ""
                )
            )

            print(
                "=" * 70
            )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()