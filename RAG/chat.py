from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
import re


# ============================================================
# CONFIGURATION
# ============================================================

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "bis_knowledge"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Normal semantic retrieval
RETRIEVAL_LIMIT = 8

# Maximum results for normal queries
MAX_RESULTS = 4

# Maximum characters allowed in final context
MAX_CONTEXT_CHARS = 12000

# Maximum size of one document
MAX_DOCUMENT_CHARS = 5000

# Exhaustive retrieval batch size
SCROLL_BATCH_SIZE = 256


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
# PRODUCT ALIASES
# ============================================================

PRODUCT_ALIASES = {

    "helmet":
        "protective_helmets_for_motorcycle_riders_-_specification_(fourth_revision)",

    "motorcycle helmet":
        "protective_helmets_for_motorcycle_riders_-_specification_(fourth_revision)",

    "bike helmet":
        "protective_helmets_for_motorcycle_riders_-_specification_(fourth_revision)",

    "pressure cooker":
        "domestic_pressure_cooker_-_specification_(seventh_revision)",

    "pressure cookers":
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

    "refrigerator":
        "refrigerator_or_combined_refrigerator_and_water-pack_freezer_intermittent_mains_powered_-_compression_cycle_-_general_requirements_and_test_methods",

    "air conditioner":
        "room_air_conditioners_specification_part_1_unitary_air_conditioners_fourth_revision",

    "ac":
        "room_air_conditioners_specification_part_1_unitary_air_conditioners_fourth_revision",

    "safety glass":
        "safety_glass_-_specification_part_1_architectural,_building_and_general_uses_(fourth_revision)",

    "electric toy":
        "safety_of_electric_toys",

    "electric toys":
        "safety_of_electric_toys",

    "tyre cord":
        "textiles_polyamide_tyre_cord_fabric_for_automotive_tyres_specification_(first_revision)",

    "tyre cord fabric":
        "textiles_polyamide_tyre_cord_fabric_for_automotive_tyres_specification_(first_revision)",

    "pvc pipe":
        "unplasticized_pvc_pipes_for_potable_water_supplies_-_specification_(fourth_revision)",

    "pvc pipes":
        "unplasticized_pvc_pipes_for_potable_water_supplies_-_specification_(fourth_revision)",

    "gas cylinder valve":
        "valve_for_compressed_gas_cylinders_excluding_liquefied_petroleum_gas_(lpg)_cylinders_-_specification_(fourth_revision)",
}


# ============================================================
# PRODUCT DETECTION
# ============================================================

def detect_product(query):
    """
    Detect one supported product from the query.
    """

    q = normalize(query)

    # Check aliases first
    # Longest aliases first prevents short aliases
    # from matching too early.
    aliases = sorted(
        PRODUCT_ALIASES.items(),
        key=lambda x: len(normalize(x[0])),
        reverse=True
    )

    for alias, product in aliases:

        if normalize(alias) in q:
            return product

    # Check complete product names
    for product in ALLOWED_PRODUCTS:

        readable = normalize(product)

        if readable in q:
            return product

    return None


# ============================================================
# PRODUCT DISPLAY NAME
# ============================================================

PRODUCT_DISPLAY_NAMES = {

    "domestic_pressure_cooker_-_specification_(seventh_revision)":
        "Domestic Pressure Cooker",

    "domestic_gas_stove_and_built_in_hob_for_use_with_lpg_specification_(sixth_revision_)":
        "Domestic Gas Stove and Built-In Hob",

    "electric_immersion_water_heaters_-_specification_(fifth_revision)":
        "Electric Immersion Water Heaters",

    "electric_iron_-_specification_(fourth_revision)":
        "Electric Iron",

    "ordinary_portland_cement_-_specification_(sixth_revision)":
        "Ordinary Portland Cement",

    "packaged_drinking_water_other_than_packaged_natural_mineral_water_specification_third_revision":
        "Packaged Drinking Water",

    "protective_helmets_for_motorcycle_riders_-_specification_(fourth_revision)":
        "Protective Helmets for Motorcycle Riders",

    "refrigerator_or_combined_refrigerator_and_water-pack_freezer_intermittent_mains_powered_-_compression_cycle_-_general_requirements_and_test_methods":
        "Refrigerator / Combined Refrigerator and Water-Pack Freezer",

    "room_air_conditioners_specification_part_1_unitary_air_conditioners_fourth_revision":
        "Room Air Conditioners",

    "safety_glass_-_specification_part_1_architectural,_building_and_general_uses_(fourth_revision)":
        "Safety Glass",

    "safety_of_electric_toys":
        "Safety of Electric Toys",

    "textiles_polyamide_tyre_cord_fabric_for_automotive_tyres_specification_(first_revision)":
        "Polyamide Tyre Cord Fabric",

    "unplasticized_pvc_pipes_for_potable_water_supplies_-_specification_(fourth_revision)":
        "Unplasticized PVC Pipes for Potable Water Supplies",

    "valve_for_compressed_gas_cylinders_excluding_liquefied_petroleum_gas_(lpg)_cylinders_-_specification_(fourth_revision)":
        "Valve for Compressed Gas Cylinders",
}


def display_product_name(product):
    return PRODUCT_DISPLAY_NAMES.get(
        product,
        product
    )


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
    Detect large archive/index documents.
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

    for source_name in NOISY_SOURCES:

        if source_name in source:
            return True

    is_numbers = re.findall(
        r"\bIS\s*\d+(?::\d{4})?\b",
        text,
        flags=re.IGNORECASE
    )

    if len(is_numbers) > 80:
        return True

    for term in NOISY_TERMS:

        if term in text_lower:
            return True

    return False


# ============================================================
# PRODUCT RELEVANCE
# ============================================================

def product_matches(payload, product):

    if not product:
        return True

    target = normalize(product)

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

    # Exact metadata match
    if product_name == target:
        return True

    # Product identifier/name inside document
    if target in payload_text:
        return True

    # Shortened product matching
    product_words = target.split()

    matching_words = sum(
        1
        for word in product_words
        if len(word) > 4 and word in payload_text
    )

    return matching_words >= 3


# ============================================================
# LABORATORY QUERY DETECTION
# ============================================================

LABORATORY_TERMS = [
    "laboratory",
    "laboratories",
    "lab",
    "labs",
    "testing laboratory",
    "testing laboratories",
    "testing lab",
    "testing labs",
    "test laboratory",
    "test laboratories",
]


EXHAUSTIVE_TERMS = [
    "how many",
    "number of",
    "count",
    "all",
    "every",
    "list all",
    "show all",
    "give all",
    "which laboratories",
    "which labs",
    "list laboratories",
    "list labs",
]


def is_laboratory_query(query):
    """
    Detect laboratory-related questions.
    """

    q = normalize(query)

    return any(
        normalize(term) in q
        for term in LABORATORY_TERMS
    )


def is_exhaustive_query(query):
    """
    Detect queries requiring all matching records.
    """

    q = normalize(query)

    return any(
        normalize(term) in q
        for term in EXHAUSTIVE_TERMS
    )


def is_exhaustive_laboratory_query(query):
    return (
        is_laboratory_query(query)
        and (
            is_exhaustive_query(query)
            or "laboratory" in normalize(query)
            or "laboratories" in normalize(query)
            or "labs" in normalize(query)
        )
    )


# ============================================================
# STANDARD EXTRACTION
# ============================================================

def extract_standard(query):
    """
    Extract an explicit IS standard from the query.

    Examples:
        IS 2347
        IS 2347:2023
        is2347:2023
    """

    if not query:
        return None

    match = re.search(
        r"\bIS\s*[-:]?\s*(\d+)(?:\s*:\s*(\d{4}))?\b",
        query,
        flags=re.IGNORECASE
    )

    if not match:
        return None

    number = match.group(1)
    year = match.group(2)

    if year:
        return f"IS {number}:{year}"

    return f"IS {number}"


def standard_matches(
    payload,
    standard
):
    """
    Check whether payload matches an explicit standard.
    """

    if not standard:
        return True

    requested = normalize(standard)

    payload_standard = normalize(
        payload.get(
            "standard_number",
            ""
        )
    )

    payload_text = normalize(
        payload.get(
            "text",
            ""
        )
    )

    if requested in payload_standard:
        return True

    if requested in payload_text:
        return True

    # Match standard number without revision year
    number_match = re.search(
        r"\d+",
        requested
    )

    if number_match:

        number = number_match.group(0)

        if number in payload_standard:
            return True

    return False


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):

    if not text:
        return ""

    text = str(text)

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    text = re.sub(
        r"[ \t]{2,}",
        " ",
        text
    )

    return text.strip()


# ============================================================
# DOCUMENT COMPACTION
# ============================================================

def compact_document(
    text,
    document_type=None
):
    """
    Compact large documents.

    Laboratory records are already small structured records,
    therefore they are preserved almost completely.
    """

    text = clean_text(text)

    if not text:
        return ""

    # Never aggressively compact laboratory records
    if document_type == "laboratory":

        return text[
            :MAX_DOCUMENT_CHARS
        ]

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
        "sampling",
        "sample size",
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

    return "\n".join(
        selected
    )[
        :MAX_DOCUMENT_CHARS
    ]


# ============================================================
# LABORATORY DEDUPLICATION
# ============================================================

def laboratory_key(payload):
    """
    Generate a stable key for laboratory deduplication.

    The same laboratory can exist in:
        complete.json
        getstandardlaboratorydetails.json

    Those should count as one laboratory.
    """

    name = normalize(
        payload.get(
            "laboratory_name",
            ""
        )
    )

    # Your actual records store the name inside text,
    # so extract it if metadata field is absent.
    if not name:

        text = str(
            payload.get(
                "text",
                ""
            )
        )

        match = re.search(
            r"(?:Name|Laboratory Name)\s*:\s*(.+)",
            text,
            flags=re.IGNORECASE
        )

        if match:
            name = normalize(
                match.group(1)
            )

    address = normalize(
        payload.get(
            "address",
            ""
        )
    )

    if not address:

        text = str(
            payload.get(
                "text",
                ""
            )
        )

        match = re.search(
            r"Address\s*:\s*(.+)",
            text,
            flags=re.IGNORECASE
        )

        if match:
            address = normalize(
                match.group(1)
            )

    standard = normalize(
        payload.get(
            "standard_number",
            ""
        )
    )

    return (
        name,
        address,
        standard
    )


# ============================================================
# EXHAUSTIVE LABORATORY RETRIEVAL
# ============================================================

def search_all_laboratories(
    query,
    product=None,
    standard=None
):
    """
    Retrieve ALL laboratory records from Qdrant.

    This does NOT depend on semantic top-k retrieval.
    """

    print("\n--- EXHAUSTIVE LABORATORY RETRIEVAL ---")

    if product:
        print(
            "Product:",
            display_product_name(product)
        )

    if standard:
        print(
            "Standard:",
            standard
        )

    # --------------------------------------------------------
    # Build exact metadata filter
    # --------------------------------------------------------

    must_conditions = [
        FieldCondition(
            key="type",
            match=MatchValue(
                value="laboratory"
            )
        )
    ]

    # If standard exists, use it as an additional
    # exact metadata condition.
    if standard:

        must_conditions.append(
            FieldCondition(
                key="standard_number",
                match=MatchValue(
                    value=standard
                )
            )
        )

    qdrant_filter = Filter(
        must=must_conditions
    )

    # --------------------------------------------------------
    # Scroll through ALL matching records
    # --------------------------------------------------------

    all_points = []

    offset = None

    while True:

        points, next_offset = client.scroll(
            collection_name=COLLECTION_NAME,
            scroll_filter=qdrant_filter,
            limit=SCROLL_BATCH_SIZE,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )

        if not points:
            break

        all_points.extend(points)

        if next_offset is None:
            break

        offset = next_offset

    print(
        "Raw laboratory records:",
        len(all_points)
    )

    # --------------------------------------------------------
    # Product filtering
    #
    # We do this after scroll because some datasets may have
    # inconsistent product metadata.
    # --------------------------------------------------------

    filtered = []

    for point in all_points:

        payload = point.payload or {}

        if not product_matches(
            payload,
            product
        ):
            continue

        if not standard_matches(
            payload,
            standard
        ):
            continue

        filtered.append(point)

    print(
        "After product/standard filtering:",
        len(filtered)
    )

    # --------------------------------------------------------
    # Deduplicate
    # --------------------------------------------------------

    unique = []

    seen = set()

    for point in filtered:

        payload = point.payload or {}

        key = laboratory_key(
            payload
        )

        # If we couldn't extract a useful laboratory name,
        # use the complete text as fallback.
        if not key[0]:

            key = (
                normalize(
                    payload.get(
                        "text",
                        ""
                    )
                ),
                "",
                normalize(
                    payload.get(
                        "standard_number",
                        ""
                    )
                )
            )

        if key in seen:
            continue

        seen.add(key)

        unique.append(point)

    print(
        "Unique laboratories:",
        len(unique)
    )

    return unique


# ============================================================
# NORMAL SEMANTIC SEARCH
# ============================================================

def semantic_search(
    query,
    limit=RETRIEVAL_LIMIT
):
    """
    Original semantic retrieval behavior.
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

    return results.points


# ============================================================
# MAIN SEARCH FUNCTION
# ============================================================

def search_knowledge(
    query,
    limit=RETRIEVAL_LIMIT
):
    """
    Smart BIS retrieval.

    Normal questions:
        semantic top-k search

    Laboratory/count/all questions:
        exhaustive Qdrant retrieval
    """

    detected_product = detect_product(
        query
    )

    explicit_standard = extract_standard(
        query
    )

    # --------------------------------------------------------
    # SPECIAL CASE:
    # Laboratory / count / all queries
    # --------------------------------------------------------

    if is_exhaustive_laboratory_query(
        query
    ):

        return search_all_laboratories(
            query=query,
            product=detected_product,
            standard=explicit_standard
        )

    # --------------------------------------------------------
    # NORMAL SEMANTIC SEARCH
    # --------------------------------------------------------

    points = semantic_search(
        query,
        limit=limit
    )

    filtered = []

    for point in points:

        payload = point.payload or {}

        text = payload.get(
            "text",
            ""
        )

        if not text.strip():
            continue

        if is_noisy_document(
            payload
        ):
            continue

        if detected_product:

            if not product_matches(
                payload,
                detected_product
            ):
                continue

        if explicit_standard:

            if not standard_matches(
                payload,
                explicit_standard
            ):
                continue

        filtered.append(point)

    # --------------------------------------------------------
    # Deduplication
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

        fingerprint = normalize(
            text[:1000]
        )

        if fingerprint in seen:
            continue

        seen.add(
            fingerprint
        )

        unique.append(
            point
        )

    # --------------------------------------------------------
    # Compact normal results
    # --------------------------------------------------------

    final_results = []

    total_chars = 0

    for point in unique:

        payload = point.payload or {}

        original_text = payload.get(
            "text",
            ""
        )

        document_type = str(
            payload.get(
                "type",
                ""
            )
        ).lower()

        compacted = compact_document(
            original_text,
            document_type
        )

        if not compacted:
            continue

        remaining = (
            MAX_CONTEXT_CHARS
            - total_chars
        )

        if remaining <= 0:
            break

        compacted = compacted[
            :remaining
        ]

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

        if len(
            final_results
        ) >= MAX_RESULTS:

            break

    return final_results


# ============================================================
# BUILD LLM CONTEXT
# ============================================================

def build_context(
    results
):
    """
    Build context for the LLM.

    Laboratory results are represented as structured
    evidence so the LLM can count unique records correctly.
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

        record_type = payload.get(
            "type",
            ""
        )

        lab_state = payload.get(
            "lab_state",
            ""
        )

        text = payload.get(
            "text",
            ""
        )

        section = (
            f"[EVIDENCE {i}]\n"
            f"Type: {record_type}\n"
            f"Product: {product}\n"
            f"Standard: {standard}\n"
            f"State: {lab_state}\n"
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

        detected_standard = extract_standard(
            question
        )

        print(
            "\nDetected product:",
            display_product_name(
                detected_product
            )
            if detected_product
            else "Not identified"
        )

        print(
            "Detected standard:",
            detected_standard
            if detected_standard
            else "Not explicitly specified"
        )

        if is_exhaustive_laboratory_query(
            question
        ):

            print(
                "Retrieval mode:",
                "EXHAUSTIVE LABORATORY SEARCH"
            )

        else:

            print(
                "Retrieval mode:",
                "SEMANTIC SEARCH"
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

            if hasattr(
                result,
                "score"
            ) and result.score is not None:

                print(
                    f"Score: "
                    f"{result.score:.4f}"
                )

            print(
                f"Type: "
                f"{payload.get('type', 'N/A')}"
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
                f"State: "
                f"{payload.get('lab_state', 'N/A')}"
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
            "\n" + "=" * 70
        )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()