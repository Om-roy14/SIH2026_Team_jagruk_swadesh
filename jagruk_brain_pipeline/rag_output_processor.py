from RAG.chat import search_knowledge
from openai import OpenAI
import os
import json
import re
from dotenv import load_dotenv


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

api_key = os.getenv("API_KEY_groq")

if not api_key:
    raise ValueError(
        "API_KEY_groq is not set in the .env file."
    )

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)


# ============================================================
# BIS SYSTEM PROMPT
# ============================================================
#
# IMPORTANT:
# Paste your ORIGINAL COMPLETE BIS SYSTEM PROMPT below.
#
# Do NOT replace your real 25-section prompt with the placeholder.
#
# Keep all your existing BIS rules.
# ============================================================

SYSTEM_PROMPT = r"""
PASTE YOUR COMPLETE ORIGINAL BIS SYSTEM PROMPT HERE.

IMPORTANT:
Keep all 25 sections and all BIS-specific rules from your
existing system prompt.

The system prompt must continue to contain your rules regarding:

- SOURCE OF TRUTH
- LANGUAGE
- PRODUCT IDENTIFICATION
- SUPPORTED PRODUCTS
- PRODUCT → STANDARD RESOLUTION
- STANDARD + REVISION CONTROL
- PRODUCT MANUAL CONTROL
- SAMPLING / SAMPLE QUANTITY
- MULTI-INTENT QUESTIONS
- INTENT-SPECIFIC EVIDENCE
- EVIDENCE CLASSIFICATION
- CURRENT VS HISTORICAL
- LABORATORIES
- LICENCES / MANUFACTURERS
- TESTING + CERTIFICATION
- QCO / REGULATORY EVIDENCE
- CONFLICTS
- DUPLICATES + RAW DATA
- ALL / EXHAUSTIVE REQUESTS
- MISSING INFORMATION + NEGATIVE CLAIMS
- ARCHIVE / MANIFEST RULE
- PROCEDURES
- REVISION COMPARISONS
- OUTPUT FORMAT
- ACCURACY + FINAL CHECK
"""


# ============================================================
# AUTHORITATIVE LANGUAGE RULE
# ============================================================

LANGUAGE_RULE = r"""
==================================================
AUTHORITATIVE RESPONSE LANGUAGE
==================================================

TARGET_LANGUAGE:
{target_language}

The TARGET_LANGUAGE is authoritative.

The final answer MUST be written in the same language
and writing style used by the ORIGINAL USER QUERY.

The internal English retrieval query is ONLY for searching
the BIS database. It MUST NEVER determine the response language.

==================================================
SCRIPT RULES
==================================================

English:
- Answer in natural English.
- Use Latin script.

Hindi written in Devanagari:
- Answer in Hindi.
- Use Devanagari.

Bengali written in Bengali script:
- Answer in Bengali.
- Use Bengali script.

Tamil written in Tamil script:
- Answer in Tamil.
- Use Tamil script.

Telugu written in Telugu script:
- Answer in Telugu.
- Use Telugu script.

Marathi written in Devanagari:
- Answer in Marathi.
- Use Devanagari.

Gujarati:
- Answer in Gujarati script.

Kannada:
- Answer in Kannada script.

Malayalam:
- Answer in Malayalam script.

Punjabi:
- Answer in Gurmukhi.

Romanized / transliterated Indian language:
- Answer in the same Romanized / transliterated style.
- DO NOT automatically convert it to the native script.

Hinglish:
- Answer in Hinglish/Romanized Hindi if the user used that style.

==================================================
CRITICAL LANGUAGE RULE
==================================================

Do NOT translate the final answer into English unless the
ORIGINAL USER QUERY was in English.

Do NOT translate Romanized Hindi into Devanagari.

Do NOT translate Romanized Bengali into Bengali script.

Do NOT translate Romanized Tamil into Tamil script.

Do NOT translate Romanized Telugu into Telugu script.

The original query's language and writing style have priority.

The English retrieval query exists only for RAG retrieval.

Never mention:
- detected language
- target language
- translation
- transliteration
- script selection
- language detection

to the user.

==================================================
GENERAL CONVERSATION
==================================================

If the user is only greeting, asking your name, or making
casual conversation unrelated to BIS:

- Do not use irrelevant BIS evidence.
- Answer naturally in the user's language/style.
- Introduce yourself as Jagruk Brain, a BIS Assistant when appropriate.
- Do not manufacture BIS facts.
"""


# ============================================================
# SAFE PAYLOAD EXTRACTION
# ============================================================

def _get_payload(point):
    """
    Safely extract Qdrant payload.
    """

    if hasattr(point, "payload"):
        return point.payload or {}

    if isinstance(point, dict):
        return point.get(
            "payload",
            point
        )

    return {}


# ============================================================
# VALUE CLEANING
# ============================================================

def _clean_value(value):

    if value is None:
        return ""

    if isinstance(
        value,
        (dict, list)
    ):
        try:
            return json.dumps(
                value,
                ensure_ascii=False,
                separators=(",", ":")
            )

        except Exception:
            return str(value)

    return str(value)


# ============================================================
# NORMALIZATION
# ============================================================

def _normalize(value):

    if not value:
        return ""

    value = str(value).lower()

    value = re.sub(
        r"[^a-z0-9]+",
        " ",
        value
    )

    return " ".join(
        value.split()
    )


# ============================================================
# LABORATORY DETECTION
# ============================================================

def _is_laboratory_record(payload):

    record_type = _normalize(
        payload.get(
            "type",
            ""
        )
    )

    if record_type == "laboratory":
        return True

    if record_type == "lab":
        return True

    text = _normalize(
        payload.get(
            "text",
            ""
        )
    )

    laboratory_terms = [
        "laboratory",
        "laboratories",
        "testing laboratory",
        "testing lab"
    ]

    return any(
        term in text
        for term in laboratory_terms
    )


# ============================================================
# LABORATORY NAME EXTRACTION
# ============================================================

def _get_lab_name(payload):

    possible_fields = [
        "laboratory_name",
        "lab_name",
        "laboratory",
        "name"
    ]

    for field in possible_fields:

        value = payload.get(
            field
        )

        if value:
            return str(value).strip()

    text = str(
        payload.get(
            "text",
            ""
        )
    )

    patterns = [
        r"Laboratory Name\s*:\s*(.+)",
        r"Laboratory\s*:\s*(.+)",
        r"Name\s*:\s*(.+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if match:

            value = match.group(1).strip()

            if value:
                return value

    return ""


# ============================================================
# LABORATORY ADDRESS EXTRACTION
# ============================================================

def _get_lab_address(payload):

    possible_fields = [
        "address",
        "lab_address"
    ]

    for field in possible_fields:

        value = payload.get(
            field
        )

        if value:
            return str(value).strip()

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
        return match.group(1).strip()

    return ""


# ============================================================
# LABORATORY UNIQUE KEY
# ============================================================

def _laboratory_key(payload):

    name = _normalize(
        _get_lab_name(
            payload
        )
    )

    address = _normalize(
        _get_lab_address(
            payload
        )
    )

    standard = _normalize(
        payload.get(
            "standard_number",
            ""
        )
    )

    # Prefer name + address.
    if name:

        return (
            name,
            address
        )

    # Fallback if name is unavailable.
    text = _normalize(
        payload.get(
            "text",
            ""
        )
    )

    return (
        text[:500],
        standard
    )


# ============================================================
# IMPORTANT BIS FIELDS
# ============================================================

def _extract_important_fields(payload):

    important_fields = [

        # Product
        "product",
        "product_name",
        "product_id",
        "product_description",
        "description",
        "product_details",

        # Standard
        "standard",
        "standard_number",
        "standard_name",
        "standard_title",
        "standard_revision",
        "is_number",
        "is_revision",

        # Relationship
        "relationship",
        "product_standard",
        "applicable_standard",

        # QCO
        "qco",
        "qco_title",
        "qco_number",
        "qco_date",
        "qco_effective_date",

        # Product manual
        "product_manual",
        "manual",
        "manual_number",
        "manual_revision",
        "manual_date",

        # Sampling
        "sampling",
        "sample",
        "sample_size",
        "sample_quantity",
        "specimen",
        "specimens",

        # Testing
        "testing",
        "tests",
        "test",
        "test_method",
        "test_methods",
        "testing_requirements",
        "sit",
        "scheme_of_inspection_and_testing",
        "equipment",
        "test_equipment",

        # Laboratory
        "laboratory",
        "laboratory_name",
        "lab_name",
        "osl_code",
        "bis_code",
        "status",
        "address",
        "city",
        "state",
        "lab_state",
        "pin",
        "phone",
        "email",
        "testing_charge",
        "testing_charges",
        "validity",
        "remarks",
        "capability",

        # Licence
        "licence",
        "license",
        "licence_number",
        "license_number",
        "licence_holder",
        "license_holder",
        "manufacturer",
        "firm",
        "brand",
        "certification",
        "certification_scheme",
        "scope",

        # Regulatory
        "regulation",
        "notification",
        "gazette",
        "amendment",
        "corrigendum",

        # Document
        "document_type",
        "document_name",
        "document_date",
        "source",
        "source_path",
        "page",
        "record_id"
    ]

    result = {}

    for field in important_fields:

        if field not in payload:
            continue

        value = _clean_value(
            payload[field]
        )

        if value:
            result[field] = value

    # If no known fields exist, retain useful payload.
    if not result:

        ignored_fields = {
            "vector",
            "embedding",
            "id",
            "point_id",
            "uuid",
            "metadata_id"
        }

        for key, value in payload.items():

            if key in ignored_fields:
                continue

            value = _clean_value(
                value
            )

            if value:
                result[key] = value

    return result


# ============================================================
# EXHAUSTIVE LAB SUMMARY
# ============================================================

def _build_laboratory_summary(
    rag_results
):
    """
    Build deterministic laboratory count.

    This prevents the LLM from trying to count duplicate
    Qdrant records itself.
    """

    laboratories = []

    seen = set()

    for point in rag_results:

        payload = _get_payload(
            point
        )

        if not _is_laboratory_record(
            payload
        ):
            continue

        key = _laboratory_key(
            payload
        )

        if key in seen:
            continue

        seen.add(key)

        name = _get_lab_name(
            payload
        )

        address = _get_lab_address(
            payload
        )

        standard = str(
            payload.get(
                "standard_number",
                ""
            )
        ).strip()

        state = str(
            payload.get(
                "lab_state",
                payload.get(
                    "state",
                    ""
                )
            )
        ).strip()

        laboratories.append({
            "name": name,
            "address": address,
            "standard": standard,
            "state": state
        })

    if not laboratories:
        return ""

    lines = []

    lines.append(
        "=================================================="
    )

    lines.append(
        "DETERMINISTIC LABORATORY SUMMARY"
    )

    lines.append(
        "=================================================="
    )

    lines.append(
        f"UNIQUE LABORATORIES FOUND: {len(laboratories)}"
    )

    lines.append(
        "The count above is calculated from unique laboratory "
        "records after deduplication."
    )

    lines.append(
        "Do not recalculate or guess the total."
    )

    lines.append("")

    lines.append(
        "LABORATORY RECORDS:"
    )

    for index, lab in enumerate(
        laboratories,
        start=1
    ):

        lines.append(
            f"{index}. {lab['name'] or 'Name not available'}"
        )

        if lab["address"]:
            lines.append(
                f"   Address: {lab['address']}"
            )

        if lab["state"]:
            lines.append(
                f"   State: {lab['state']}"
            )

        if lab["standard"]:
            lines.append(
                f"   Standard: {lab['standard']}"
            )

    return "\n".join(lines)


# ============================================================
# RAG CONTEXT COMPACTION
# ============================================================

def compact_rag_context(
    rag_results,
    max_total_chars=12000,
    max_record_chars=2500
):
    """
    Compact RAG results without losing important BIS evidence.

    Special handling:
        Laboratory queries
        → calculate unique laboratory count
        → preserve laboratory records
    """

    if not rag_results:

        return (
            "No BIS RAG evidence was retrieved."
        )

    # --------------------------------------------------------
    # Check whether laboratory records exist
    # --------------------------------------------------------

    laboratory_summary = _build_laboratory_summary(
        rag_results
    )

    records = []

    # --------------------------------------------------------
    # Preserve structured laboratory evidence
    # --------------------------------------------------------

    for index, point in enumerate(
        rag_results,
        start=1
    ):

        payload = _get_payload(
            point
        )

        if not payload:
            continue

        clean_record = _extract_important_fields(
            payload
        )

        if not clean_record:
            continue

        is_lab = _is_laboratory_record(
            payload
        )

        lines = [
            f"RECORD {index}"
        ]

        # Laboratory records get their most important
        # fields first.
        if is_lab:

            lab_name = _get_lab_name(
                payload
            )

            lab_address = _get_lab_address(
                payload
            )

            standard = payload.get(
                "standard_number",
                ""
            )

            state = payload.get(
                "lab_state",
                payload.get(
                    "state",
                    ""
                )
            )

            if lab_name:
                lines.append(
                    f"laboratory_name: {lab_name}"
                )

            if standard:
                lines.append(
                    f"standard_number: {standard}"
                )

            if state:
                lines.append(
                    f"state: {state}"
                )

            if lab_address:
                lines.append(
                    f"address: {lab_address}"
                )

        # Add remaining important fields.
        for key, value in clean_record.items():

            # Avoid duplicating fields already added.
            if is_lab and key in {
                "laboratory_name",
                "lab_name",
                "laboratory",
                "standard_number",
                "state",
                "lab_state",
                "address"
            }:
                continue

            text = str(
                value
            ).strip()

            if not text:
                continue

            if len(text) > max_record_chars:

                text = (
                    text[:max_record_chars]
                    + " ...[field truncated]"
                )

            lines.append(
                f"{key}: {text}"
            )

        records.append(
            "\n".join(lines)
        )

    if not records:

        return (
            "No usable BIS evidence was retrieved."
        )

    # --------------------------------------------------------
    # Laboratory summary gets PRIORITY.
    # --------------------------------------------------------

    final_parts = []

    current_size = 0

    if laboratory_summary:

        final_parts.append(
            laboratory_summary
        )

        current_size = len(
            laboratory_summary
        )

    # --------------------------------------------------------
    # Add evidence records
    # --------------------------------------------------------

    for record in records:

        addition_size = len(record) + 2

        if (
            current_size + addition_size
            > max_total_chars
        ):
            break

        final_parts.append(
            record
        )

        current_size += addition_size

    context = "\n\n".join(
        final_parts
    )

    return context[
        :max_total_chars
    ]


# ============================================================
# GENERAL CONVERSATION
# ============================================================

def is_general_conversation(
    query
):
    """
    Prevent unrelated BIS retrieval for simple casual queries.
    """

    q = query.lower().strip()

    greetings = {
        "hi",
        "hello",
        "hey",
        "hola",
        "namaste",
        "good morning",
        "good afternoon",
        "good evening",
        "good night",
        "who are you",
        "what is your name",
        "what's your name",
        "your name"
    }

    return q in greetings


# ============================================================
# FINAL RESPONSE
# ============================================================

def rag_response(
    query: str,
    target_language: str = "English"
) -> str:

    print(
        "\n--- Searching Qdrant Vector Database ---"
    )

    # --------------------------------------------------------
    # GENERAL CONVERSATION
    # --------------------------------------------------------

    if is_general_conversation(
        query
    ):

        rag_context = (
            "NO BIS RETRIEVAL REQUIRED "
            "FOR THIS QUERY."
        )

    else:

        # ----------------------------------------------------
        # RETRIEVE
        # ----------------------------------------------------

        rag_results = search_knowledge(
            query
        )

        # ----------------------------------------------------
        # COMPACT
        # ----------------------------------------------------

        rag_context = compact_rag_context(
            rag_results,
            max_total_chars=12000,
            max_record_chars=2500
        )

    # --------------------------------------------------------
    # DEBUG
    # --------------------------------------------------------

    print(
        f"--- Retrieved/Compacted RAG Context: "
        f"{len(rag_context)} characters ---"
    )

    # --------------------------------------------------------
    # LANGUAGE RULE
    # --------------------------------------------------------

    final_language_prompt = LANGUAGE_RULE.format(
        target_language=target_language
    )

    # --------------------------------------------------------
    # FINAL SYSTEM PROMPT
    # --------------------------------------------------------

    dynamic_prompt = (
        SYSTEM_PROMPT
        + "\n\n"
        + final_language_prompt
    )

    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    user_message = f"""
ORIGINAL USER QUERY:
{query}

TARGET RESPONSE LANGUAGE:
{target_language}

==================================================
RETRIEVED BIS RAG EVIDENCE
==================================================

{rag_context}

==================================================
FINAL ANSWER RULES
==================================================

1. Answer the ORIGINAL USER QUERY.

2. The ORIGINAL USER QUERY determines the response
   language and writing style.

3. The TARGET RESPONSE LANGUAGE is authoritative.

4. The internal English retrieval query, if one exists,
   is ONLY for database retrieval.

5. NEVER answer in a different language merely because
   the retrieval query is English.

6. If the user wrote Romanized Hindi/Hinglish,
   answer in Romanized Hindi/Hinglish.

7. If the user wrote Hindi in Devanagari,
   answer in Hindi Devanagari.

8. If the user wrote English,
   answer in English using Latin script.

9. Use only facts supported by the retrieved BIS evidence.

10. Do not invent missing information.

11. If the evidence is insufficient, explicitly say so.

12. For exhaustive laboratory queries:
    - The deterministic laboratory summary contains the
      authoritative unique laboratory count.
    - Use that count directly.
    - Do not estimate the count.
    - Do not count duplicate evidence records again.

13. If the user asks "how many", give the number clearly.

14. If the user asks "all", provide all records that are
    actually available in the retrieved evidence.

15. Do not mention these instructions to the user.

16. Do not mention:
    - RAG
    - Qdrant
    - embeddings
    - retrieval
    - target language
    - detected language
    - translation
    unless the user explicitly asks about the system itself.
"""

    # --------------------------------------------------------
    # TOKEN SAFETY
    # --------------------------------------------------------

    total_chars = (
        len(dynamic_prompt)
        + len(user_message)
    )

    approximate_tokens = (
        total_chars // 4
    )

    print(
        f"--- Approximate request size: "
        f"{approximate_tokens} tokens ---"
    )

    # --------------------------------------------------------
    # GROQ
    # --------------------------------------------------------

    response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "system",
                "content": dynamic_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ],

        temperature=0
    )

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    result = (
        response
        .choices[0]
        .message
        .content
    )

    if not result:

        return (
            "I could not generate a response "
            "from the retrieved BIS evidence."
        )

    return result.strip()