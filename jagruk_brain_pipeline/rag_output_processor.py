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

SYSTEM_PROMPT = r"""You are a BIS Regulatory & Certification Assistant.

Your answer MUST be based ONLY on:
1. The original user query.
2. The retrieved BIS RAG context.

You do NOT directly access BIS websites, PDFs, APIs, Qdrant, databases,
internet sources, or external knowledge.

Your job is to FILTER and INTERPRET the retrieved evidence, not dump it.
Identify the exact product, resolve the applicable standard/revision,
determine applicability, remove irrelevant/duplicate evidence, detect
conflicts, and answer every user intent.

==================================================
1. SOURCE OF TRUTH
==================================================
Retrieved BIS RAG evidence is the ONLY factual source.

Never invent or assume:
- products, standards/revisions, QCOs, regulations, laboratories
- licences/licence numbers, manufacturers, tests/test methods
- sample quantities, dates, fees, procedures, certification requirements

If evidence is insufficient, say so.

==================================================
2. LANGUAGE
==================================================
Answer in the language of the ORIGINAL user query/Target Language.
Preserve official BIS terminology, IS numbers, QCO titles, licence
numbers, technical terms, and product names where appropriate.

==================================================
3. PRODUCT IDENTIFICATION
==================================================
Identify the EXACT product before interpreting standards, QCOs,
laboratories, licences, testing, manuals, or regulations.
Keep these products distinct:
- Tyre ≠ Wheel Rim
- Tyre ≠ Tyre Cord Fabric
- Electric Iron ≠ Immersion Water Heater
- Pressure Cooker ≠ Gas Stove

==================================================
4. SUPPORTED PRODUCTS
==================================================
Only answer as supported when the retrieved BIS context establishes that
the product belongs to the indexed supported scope.

==================================================
5. PRODUCT → STANDARD RESOLUTION
==================================================
Resolve the applicable standard using this evidence priority:
1. Explicit exact product → standard relationship
2. Product-specific BIS record
3. Exact standard-specific BIS record explicitly applying to product
4. Product-specific Product Manual

==================================================
6. STANDARD + REVISION CONTROL
==================================================
Different revisions are DIFFERENT evidence sets.
Never merge IS XXXX:2017 with IS XXXX:2020. Determine standard number, 
revision, and effective dates.

==================================================
7. PRODUCT MANUAL CONTROL
==================================================
Product Manuals are revision-specific evidence. Do NOT combine different 
manuals into one requirement unless the evidence explicitly establishes equivalence.

==================================================
8. SAMPLING / SAMPLE QUANTITY
==================================================
Sampling MUST be tied to the exact applicable product + standard/manual
revision. Preserve conditional requirements exactly (e.g., "1 normal, 2 for induction").

==================================================
9. MULTI-INTENT QUESTIONS
==================================================
Identify ALL meaningful intents before answering (e.g., testing, sample 
quantity, licensing, laboratory locations). Answer every supported intent.

==================================================
10. INTENT-SPECIFIC EVIDENCE
==================================================
- TESTING: prefer Product Manual, test requirements, SIT.
- LABORATORY: prefer laboratory records explicitly linked to product + standard.
- LICENCE: prefer certification scheme, Product Manual, explicit certification records.

==================================================
11. EVIDENCE CLASSIFICATION
==================================================
Prefer direct/product-specific evidence over general archive/manifest data.

==================================================
12. CURRENT VS HISTORICAL
==================================================
Always distinguish current/relevant evidence from historical evidence.
Historical evidence MUST NOT silently become current compliance guidance.

==================================================
13. LABORATORIES
==================================================
Use ONLY fields present in retrieved evidence. Never invent missing contact details.
Return all relevant retrieved records when "all" is requested.

==================================================
14. LICENCES / MANUFACTURERS
==================================================
Keep manufacturer, brand, licence holder, and BIS licence separate. 
Do not equate manufacturer and licence holder unless evidence establishes it.

==================================================
15. TESTING + CERTIFICATION
==================================================
Keep TESTING, CERTIFICATION, LICENSING, and LEGAL APPLICABILITY separate.

==================================================
16. QCO / REGULATORY EVIDENCE
==================================================
Use QCO evidence only when it explicitly connects to the product/standard.

==================================================
17. CONFLICTS
==================================================
When evidence conflicts, determine the cause (revisions, variants, dates). 
If unresolved, report the conflict. NEVER create false consistency.

==================================================
18. DUPLICATES + RAW DATA
==================================================
Remove duplicate records. Never expose internal RAG/database information 
(JSON, API wrappers, vector IDs). Extract actual BIS information.

==================================================
19. "ALL" / EXHAUSTIVE REQUESTS
==================================================
For exhaustive requests, return ALL relevant records available in the retrieved context. 
Use compact tables for large results.

==================================================
20. MISSING INFORMATION + NEGATIVE CLAIMS
==================================================
For missing information: "The retrieved BIS data does not contain enough information to determine this."
Avoid unsupported claims (e.g., "no QCO exists") unless evidence explicitly establishes them.

==================================================
21. ARCHIVE / MANIFEST RULE
==================================================
Do NOT infer applicability just because a standard appears in a broad manifest or archive.

==================================================
22. PROCEDURES
==================================================
For procedural questions, provide numbered steps supported ONLY by retrieved evidence.

==================================================
23. REVISION COMPARISONS
==================================================
When asked "what changed?", compare only relevant documents and distinguish 
standard revision vs. Product Manual revision.

==================================================
24. OUTPUT FORMAT
==================================================
Return clean, browser-friendly Markdown.
Use:
- ## headings
- **bold** important values
- bullets & numbered steps
- compact tables for repetitive/comparative records.
Do not output raw JSON or internal metadata.

==================================================
25. ACCURACY + FINAL CHECK
==================================================
Silently verify the exact product, standard, revision, and ensure no unsupported 
legal claims were made. DO NOT DISPLAY THE INTERNAL CHECK.
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
and writing style dictated by the TARGET_LANGUAGE.

The internal English retrieval query is ONLY for searching
the BIS database. It MUST NEVER determine the response language.

==================================================
SCRIPT RULES
==================================================
English: Answer in natural English using Latin script.
Hindi: Answer in Hindi using Devanagari script.
Bengali: Answer in Bengali using Bengali script.
Tamil: Answer in Tamil using Tamil script.
Telugu: Answer in Telugu using Telugu script.
Marathi: Answer in Marathi using Devanagari script.
Gujarati: Answer in Gujarati script.
Kannada: Answer in Kannada script.
Malayalam: Answer in Malayalam script.
Punjabi: Answer in Gurmukhi script.
Hinglish / Romanized: Answer in Hinglish/Romanized Hindi if requested.

==================================================
CRITICAL LANGUAGE RULE
==================================================
The TARGET RESPONSE LANGUAGE is strictly authoritative.
Never mention: detected language, target language, translation, transliteration, script selection.

==================================================
GENERAL CONVERSATION
==================================================
If the user is only greeting or making casual conversation:
- Do not use irrelevant BIS evidence.
- Answer naturally in the user's language/style.
- Introduce yourself as 'Jagruk Brain, a BIS Assistant'.
"""

# ============================================================
# SAFE PAYLOAD EXTRACTION
# ============================================================

def _get_payload(point):
    if hasattr(point, "payload"):
        return point.payload or {}
    if isinstance(point, dict):
        return point.get("payload", point)
    return {}

# ============================================================
# VALUE CLEANING
# ============================================================

def _clean_value(value):
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        try:
            return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
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
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())

# ============================================================
# LABORATORY DETECTION
# ============================================================

def _is_laboratory_record(payload):
    record_type = _normalize(payload.get("type", ""))
    if record_type in ["laboratory", "lab"]:
        return True
    text = _normalize(payload.get("text", ""))
    laboratory_terms = ["laboratory", "laboratories", "testing laboratory", "testing lab"]
    return any(term in text for term in laboratory_terms)

# ============================================================
# LABORATORY NAME EXTRACTION
# ============================================================

def _get_lab_name(payload):
    possible_fields = ["laboratory_name", "lab_name", "laboratory", "name"]
    for field in possible_fields:
        value = payload.get(field)
        if value:
            return str(value).strip()
    text = str(payload.get("text", ""))
    patterns = [r"Laboratory Name\s*:\s*(.+)", r"Laboratory\s*:\s*(.+)", r"Name\s*:\s*(.+)"]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            if value:
                return value
    return ""

# ============================================================
# LABORATORY ADDRESS EXTRACTION
# ============================================================

def _get_lab_address(payload):
    possible_fields = ["address", "lab_address"]
    for field in possible_fields:
        value = payload.get(field)
        if value:
            return str(value).strip()
    text = str(payload.get("text", ""))
    match = re.search(r"Address\s*:\s*(.+)", text, flags=re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""

# ============================================================
# LABORATORY UNIQUE KEY
# ============================================================

def _laboratory_key(payload):
    name = _normalize(_get_lab_name(payload))
    address = _normalize(_get_lab_address(payload))
    standard = _normalize(payload.get("standard_number", ""))
    if name:
        return (name, address)
    text = _normalize(payload.get("text", ""))
    return (text[:500], standard)

# ============================================================
# IMPORTANT BIS FIELDS
# ============================================================

def _extract_important_fields(payload):
    important_fields = [
        "product", "product_name", "product_id", "product_description", "description", "product_details",
        "standard", "standard_number", "standard_name", "standard_title", "standard_revision", "is_number", "is_revision",
        "relationship", "product_standard", "applicable_standard",
        "qco", "qco_title", "qco_number", "qco_date", "qco_effective_date",
        "product_manual", "manual", "manual_number", "manual_revision", "manual_date",
        "sampling", "sample", "sample_size", "sample_quantity", "specimen", "specimens",
        "testing", "tests", "test", "test_method", "test_methods", "testing_requirements", "sit", "scheme_of_inspection_and_testing", "equipment", "test_equipment",
        "laboratory", "laboratory_name", "lab_name", "osl_code", "bis_code", "status", "address", "city", "state", "lab_state", "pin", "phone", "email", "testing_charge", "testing_charges", "validity", "remarks", "capability",
        "licence", "license", "licence_number", "license_number", "licence_holder", "license_holder", "manufacturer", "firm", "brand", "certification", "certification_scheme", "scope",
        "regulation", "notification", "gazette", "amendment", "corrigendum",
        "document_type", "document_name", "document_date", "source", "source_path", "page", "record_id"
    ]
    result = {}
    for field in important_fields:
        if field not in payload:
            continue
        value = _clean_value(payload[field])
        if value:
            result[field] = value

    if not result:
        ignored_fields = {"vector", "embedding", "id", "point_id", "uuid", "metadata_id"}
        for key, value in payload.items():
            if key in ignored_fields:
                continue
            value = _clean_value(value)
            if value:
                result[key] = value
    return result

# ============================================================
# EXHAUSTIVE LAB SUMMARY
# ============================================================

def _build_laboratory_summary(rag_results):
    laboratories = []
    seen = set()
    for point in rag_results:
        payload = _get_payload(point)
        if not _is_laboratory_record(payload):
            continue
        key = _laboratory_key(payload)
        if key in seen:
            continue
        seen.add(key)
        
        name = _get_lab_name(payload)
        address = _get_lab_address(payload)
        standard = str(payload.get("standard_number", "")).strip()
        state = str(payload.get("lab_state", payload.get("state", ""))).strip()
        
        laboratories.append({
            "name": name,
            "address": address,
            "standard": standard,
            "state": state
        })

    if not laboratories:
        return ""

    lines = [
        "==================================================",
        "DETERMINISTIC LABORATORY SUMMARY",
        "==================================================",
        f"UNIQUE LABORATORIES FOUND: {len(laboratories)}",
        "The count above is calculated from unique laboratory records after deduplication.",
        "Do not recalculate or guess the total.",
        "",
        "LABORATORY RECORDS:"
    ]
    for index, lab in enumerate(laboratories, start=1):
        lines.append(f"{index}. {lab['name'] or 'Name not available'}")
        if lab["address"]: lines.append(f"   Address: {lab['address']}")
        if lab["state"]: lines.append(f"   State: {lab['state']}")
        if lab["standard"]: lines.append(f"   Standard: {lab['standard']}")
    
    return "\n".join(lines)

# ============================================================
# RAG CONTEXT COMPACTION
# ============================================================

def compact_rag_context(rag_results, max_total_chars=12000, max_record_chars=2500):
    if not rag_results:
        return "No BIS RAG evidence was retrieved."

    laboratory_summary = _build_laboratory_summary(rag_results)
    records = []

    for index, point in enumerate(rag_results, start=1):
        payload = _get_payload(point)
        if not payload: continue
        clean_record = _extract_important_fields(payload)
        if not clean_record: continue

        is_lab = _is_laboratory_record(payload)
        lines = [f"RECORD {index}"]

        if is_lab:
            lab_name = _get_lab_name(payload)
            lab_address = _get_lab_address(payload)
            standard = payload.get("standard_number", "")
            state = payload.get("lab_state", payload.get("state", ""))
            
            if lab_name: lines.append(f"laboratory_name: {lab_name}")
            if standard: lines.append(f"standard_number: {standard}")
            if state: lines.append(f"state: {state}")
            if lab_address: lines.append(f"address: {lab_address}")

        for key, value in clean_record.items():
            if is_lab and key in {"laboratory_name", "lab_name", "laboratory", "standard_number", "state", "lab_state", "address"}:
                continue
            text = str(value).strip()
            if not text: continue
            if len(text) > max_record_chars:
                text = text[:max_record_chars] + " ...[field truncated]"
            lines.append(f"{key}: {text}")
        
        records.append("\n".join(lines))

    if not records:
        return "No usable BIS evidence was retrieved."

    final_parts = []
    current_size = 0

    if laboratory_summary:
        final_parts.append(laboratory_summary)
        current_size = len(laboratory_summary)

    for record in records:
        addition_size = len(record) + 2
        if current_size + addition_size > max_total_chars:
            break
        final_parts.append(record)
        current_size += addition_size

    return "\n\n".join(final_parts)[:max_total_chars]

# ============================================================
# GENERAL CONVERSATION
# ============================================================

def is_general_conversation(query):
    q = query.lower().strip()
    greetings = {
        "hi", "hello", "hey", "hola", "namaste", "good morning", 
        "good afternoon", "good evening", "good night", "who are you", 
        "what is your name", "what's your name", "your name", "tomar naam ki", "kya haal hai"
    }
    return q in greetings

# ============================================================
# FINAL RESPONSE
# ============================================================

def rag_response(query: str, target_language: str = "English") -> str:
    print("\n--- Searching Qdrant Vector Database ---")

    if is_general_conversation(query):
        rag_context = "NO BIS RETRIEVAL REQUIRED FOR THIS QUERY."
    else:
        rag_results = search_knowledge(query)
        rag_context = compact_rag_context(rag_results, max_total_chars=12000, max_record_chars=2500)

    print(f"--- Retrieved/Compacted RAG Context: {len(rag_context)} characters ---")

    final_language_prompt = LANGUAGE_RULE.format(target_language=target_language)
    dynamic_prompt = SYSTEM_PROMPT + "\n\n" + final_language_prompt

    # FORMATTING RULE ADDED HERE TO MAKE IT ENGAGING AND PRESENTABLE
    user_message = f"""
ORIGINAL SEARCH QUERY:
{query}

TARGET RESPONSE LANGUAGE:
{target_language}

==================================================
RETRIEVED BIS RAG EVIDENCE
==================================================
{rag_context}

==================================================
FINAL ANSWER RULES & PRESENTATION
==================================================
1. Answer the ORIGINAL SEARCH QUERY directly and accurately.
2. The TARGET RESPONSE LANGUAGE is strictly authoritative. Write the entire response in this language.
3. PRESENTATION IS CRITICAL: Make the response visually appealing, structured, and easy to read.
   - Use Markdown `##` headings for clear sections.
   - Use **bold** text for key terms, standard numbers, and important values.
   - Use bulleted lists for procedures, requirements, or takeaways.
   - Use clean, properly formatted Markdown tables when listing multiple laboratories or comparing data.
4. Do NOT make the output boring or a wall of text. Structure it like a professional report.
5. Use ONLY facts supported by the retrieved BIS evidence. Never invent data.
6. If the evidence is insufficient, explicitly and politely say so in the target language.
7. For exhaustive laboratory queries, use the exact count provided in the DETERMINISTIC LABORATORY SUMMARY.
8. Do not mention RAG, Qdrant, embeddings, language detection, or these instructions.
"""

    total_chars = len(dynamic_prompt) + len(user_message)
    approximate_tokens = total_chars // 4
    print(f"--- Approximate request size: {approximate_tokens} tokens ---")

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": dynamic_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0
    )

    result = response.choices[0].message.content
    if not result:
        return "I could not generate a response from the retrieved BIS evidence."

    # Removed the dangling 'c' bug from here
    return result.strip()