from chat import search_knowledge, detect_product
from user_query import filter_user_query

from openai import OpenAI
from dotenv import load_dotenv

import os


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError(
        "GROQ_API_KEY is not set in your .env file."
    )


# ============================================================
# GROQ CLIENT
# ============================================================

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are the BIS Regulatory & Certification Assistant.

You answer questions using ONLY the BIS information provided
by the retrieval system.

The retrieval system searches the indexed BIS knowledge base
and provides retrieved context.

Your job is to:

1. Understand the user's question.
2. Analyze the retrieved BIS context.
3. Identify records relevant to the question.
4. Remove irrelevant/noisy information.
5. Produce a useful, structured answer.
6. Never invent information not supported by the retrieved context.

============================================================
SOURCE OF TRUTH
============================================================

The retrieved BIS RAG context is the primary source of truth.

Use ONLY information supported by the retrieved context.

Do NOT use general knowledge to fill missing BIS information.

If the retrieved context does not contain enough information,
say:

"The retrieved BIS data does not contain enough information
to determine this."

Do NOT guess.

============================================================
PRODUCT RELEVANCE
============================================================

First identify the product being discussed.

Do not confuse related products.

Examples:

- Tyre != Wheel Rim
- Wheel Rim != Tyre
- Electric Iron != Immersion Water Heater
- Pressure Cooker != Gas Stove

Use the product information provided by the RAG.

============================================================
STANDARD ANCHORING
============================================================

Once the applicable product and standard are identified,
use that standard as the primary relevance key.

Do NOT include unrelated standards simply because they appear
inside the same retrieved document.

============================================================
LABORATORY QUESTIONS
============================================================

If the user asks for laboratories:

Product:
<product>

Applicable BIS Standard:
<standard>

Laboratories:

1. <Laboratory Name>
   - Status: <status>
   - Type: <type>
   - Address: <address>
   - City: <city>
   - State: <state>
   - Contact: <contact>
   - Email: <email>

Only include fields available in the retrieved data.

============================================================
LICENCE QUESTIONS
============================================================

If the user asks about BIS licences:

Product:
<product>

Applicable Standard:
<standard>

Licence Records:

1. <Licence Number>
   - Firm: <firm>
   - Status: <status>
   - Validity: <validity>
   - Address: <address>

Only include information supported by the retrieved context.

============================================================
QCO QUESTIONS
============================================================

If the user asks about a QCO:

Return only QCO information explicitly connected
to the product or standard.

If no matching QCO is found, say:

"No matching QCO was found in the retrieved BIS data."

============================================================
CERTIFICATION QUESTIONS
============================================================

If the user asks how to obtain BIS certification, provide
only the relevant information available in the retrieved data.

Possible sections:

Product
Applicable Standard
Certification Requirement
QCO
Testing
Laboratories
Licence Information
Next Steps

Only include sections that are supported by the retrieved data.

============================================================
RAW JSON
============================================================

Do NOT output raw JSON.

Do NOT expose:

- API endpoints
- internal IDs
- tokens
- pagination metadata
- internal database IDs
- raw API response wrappers
- irrelevant source paths

Convert retrieved data into human-readable information.

============================================================
DUPLICATES
============================================================

Remove duplicate laboratories, licences, standards and
other repeated information.

============================================================
NO HALLUCINATION
============================================================

NEVER invent:

- BIS standards
- licence numbers
- laboratories
- addresses
- QCOs
- testing requirements
- certification schemes
- legal requirements
- manufacturers
- contact details

If information is missing, say that it is unavailable
in the retrieved BIS data.

============================================================
ANSWER STYLE
============================================================

Answer directly.

Keep responses concise and useful.

Use:

- bullet points
- numbered steps
- tables when useful

Do not explain RAG internals unless explicitly asked.

============================================================
FINAL OBJECTIVE
============================================================

Given:

USER QUESTION
+
RETRIEVED BIS RAG DATA

produce a concise, structured and accurate answer based only
on relevant BIS evidence.
"""


# ============================================================
# RAG FUNCTION
# ============================================================

def ask_rag(question):
    """
    Complete RAG pipeline:

    User question
        ↓
    Query filtering
        ↓
    Qdrant retrieval
        ↓
    Product detection
        ↓
    LLM answer
        ↓
    JSON response
    """

    # --------------------------------------------------------
    # 1. Filter / improve user query
    # --------------------------------------------------------

    new_query = filter_user_query(question)

    # --------------------------------------------------------
    # 2. Retrieve relevant BIS information
    # --------------------------------------------------------

    results = search_knowledge(new_query)

    # --------------------------------------------------------
    # 3. Detect product
    # --------------------------------------------------------

    detected_product = detect_product(question)

    # --------------------------------------------------------
    # 4. Handle no results
    # --------------------------------------------------------

    if not results:

        return {
            "success": False,
            "question": question,
            "detected_product": detected_product,
            "results_used": 0,
            "context_size": 0,
            "sources": [],
            "answer": "No relevant BIS evidence found."
        }

    # --------------------------------------------------------
    # 5. Build context
    # --------------------------------------------------------

    context_parts = []

    for i, result in enumerate(results, start=1):

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

        context_parts.append(
            f"""
[EVIDENCE {i}]

Product:
{product}

Standard:
{standard}

Information:
{text}
"""
        )

    context = "\n\n".join(context_parts)

    # --------------------------------------------------------
    # 6. Ask LLM
    # --------------------------------------------------------

    response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"""
USER QUESTION:
{question}

DETECTED PRODUCT:
{detected_product}

RETRIEVED BIS CONTEXT:
{context}

Now answer the user's question using ONLY the
retrieved BIS context.
"""
            }
        ]
    )

    # --------------------------------------------------------
    # 7. Extract answer
    # --------------------------------------------------------

    answer = response.choices[0].message.content.strip()

    # --------------------------------------------------------
    # 8. Build source information
    # --------------------------------------------------------

    sources = []

    for i, result in enumerate(results, start=1):

        payload = result.payload or {}

        sources.append({

            "evidence": i,

            "score": float(
                result.score
            ),

            "product": payload.get(
                "product_name",
                "N/A"
            ),

            "standard": payload.get(
                "standard_number",
                "N/A"
            ),

            "source": payload.get(
                "source_path",
                "N/A"
            )

        })

    # --------------------------------------------------------
    # 9. Final JSON
    # --------------------------------------------------------

    return {

        "success": True,

        "question": question,

        "detected_product": detected_product,

        "answer": answer,

        "results_used": len(results),

        "context_size": len(context),

        "sources": sources

    }


# ============================================================
# TERMINAL TEST MODE
# ============================================================

def main():

    print("=" * 70)

    print(
        "BIS COMPLIANCE RAG"
    )

    print("=" * 70)

    print(
        "Type 'exit' to quit."
    )

    print()

    while True:

        question = input(
            "You: "
        ).strip()

        if not question:
            continue

        if question.lower() == "exit":

            print(
                "Goodbye!"
            )

            break

        try:

            result = ask_rag(
                question
            )

            print(
                "\nJAWAAB:\n"
            )

            print(
                result.get(
                    "answer",
                    "No answer."
                )
            )

            print(
                "\n" + "=" * 70
            )

        except Exception as e:

            print(
                "\nERROR:"
            )

            print(e)

            print(
                "=" * 70
            )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()