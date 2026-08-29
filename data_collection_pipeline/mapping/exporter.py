# ============================================================
# EXPORTER
# ============================================================
#
# Responsible for:
#   1. Saving mapped data as JSON
#   2. Building RAG-ready records
#
# RAG record structure:
#
# {
#     "rag_id": "...",
#     "product_id": "...",
#     "product_name": "...",
#     "product_slug": "...",
#
#     "standards": [...],
#     "qcos": [...],
#     "regulations": [...],
#
#     "relationships": [...],
#
#     "text": "...",
#
#     "metadata": {
#         ...
#     }
# }
#
# ============================================================

import json

from .config import OUTPUT_DIR
from .normalizer import normalize_standard


# ============================================================
# SAVE JSON
# ============================================================

def save_json(filename, data):
    """
    Save any Python object as formatted JSON.
    """

    output_path = OUTPUT_DIR / filename

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with output_path.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )

    return output_path


# ============================================================
# HELPERS
# ============================================================

def safe_list(value):
    """
    Always return a list.
    """

    if isinstance(value, list):
        return value

    if value is None:
        return []

    return [value]


def get_product_standards(product):
    """
    Return normalized standards belonging to a product.
    """

    standards = []

    for raw_standard in safe_list(
        product.get("standards", [])
    ):

        standard = normalize_standard(
            raw_standard
        )

        if standard and standard not in standards:
            standards.append(standard)

    return standards


def get_standard_records(
    product,
    standards
):
    """
    Find complete standard records belonging
    to the current product.
    """

    product_standards = set(
        get_product_standards(product)
    )

    matched = []

    for standard in standards:

        standard_number = normalize_standard(
            standard.get(
                "standard_number"
            )
        )

        if standard_number in product_standards:

            matched.append({

                "standard_id":
                    standard.get(
                        "standard_id"
                    ),

                "standard_number":
                    standard_number,

                "products":
                    standard.get(
                        "products",
                        []
                    )

            })

    return matched


def get_qco_records(
    product,
    qcos,
    relationships
):
    """
    Find QCOs connected to the product.

    Relationships are the primary source of truth.
    """

    product_id = product.get(
        "product_id"
    )

    qco_ids = set()

    # --------------------------------------------------------
    # Find QCO IDs from relationships
    # --------------------------------------------------------

    for relationship in relationships:

        if (
            relationship.get(
                "source_type"
            ) != "product"
        ):
            continue

        if (
            relationship.get(
                "source_id"
            ) != product_id
        ):
            continue

        if (
            relationship.get(
                "relationship"
            ) != "SUBJECT_TO"
        ):
            continue

        target_id = relationship.get(
            "target_id"
        )

        if target_id:
            qco_ids.add(target_id)

    # --------------------------------------------------------
    # Build complete QCO objects
    # --------------------------------------------------------

    matched = []

    for qco in qcos:

        if qco.get("qco_id") in qco_ids:

            matched.append({

                "qco_id":
                    qco.get(
                        "qco_id"
                    ),

                "title":
                    qco.get(
                        "title"
                    ),

                "notification_number":
                    qco.get(
                        "notification_number"
                    ),

                "notification_date":
                    qco.get(
                        "notification_date"
                    ),

                "effective_date":
                    qco.get(
                        "effective_date"
                    ),

                "issuing_department":
                    qco.get(
                        "issuing_department"
                    ),

                "certifying_authority":
                    qco.get(
                        "certifying_authority"
                    ),

                "scheme":
                    qco.get(
                        "scheme"
                    ),

                "declared_standard":
                    qco.get(
                        "declared_standard"
                    ),

                "standards_found":
                    qco.get(
                        "standards_found",
                        []
                    ),

                "source_path":
                    qco.get(
                        "source_path"
                    )

            })

    return matched


def get_regulation_records(
    product,
    regulations,
    relationships
):
    """
    Find regulations connected to the product.
    """

    product_id = product.get(
        "product_id"
    )

    regulation_ids = set()

    # --------------------------------------------------------
    # Find regulation IDs from relationships
    # --------------------------------------------------------

    for relationship in relationships:

        if (
            relationship.get(
                "source_type"
            ) != "product"
        ):
            continue

        if (
            relationship.get(
                "source_id"
            ) != product_id
        ):
            continue

        if (
            relationship.get(
                "relationship"
            ) != "REGULATED_BY"
        ):
            continue

        target_id = relationship.get(
            "target_id"
        )

        if target_id:
            regulation_ids.add(
                target_id
            )

    # --------------------------------------------------------
    # Build complete regulation objects
    # --------------------------------------------------------

    matched = []

    for regulation in regulations:

        if (
            regulation.get(
                "regulation_id"
            )
            not in regulation_ids
        ):
            continue

        matched.append({

            "regulation_id":
                regulation.get(
                    "regulation_id"
                ),

            "document_name":
                regulation.get(
                    "document_name"
                ),

            "source":
                regulation.get(
                    "source"
                ),

            "standards_found":
                regulation.get(
                    "standards_found",
                    []
                ),

            "source_path":
                regulation.get(
                    "source_path"
                )

        })

    return matched


def get_product_relationships(
    product,
    relationships
):
    """
    Return all relationships belonging to a product.
    """

    product_id = product.get(
        "product_id"
    )

    result = []

    for relationship in relationships:

        if (
            relationship.get(
                "source_id"
            )
            != product_id
        ):
            continue

        result.append({

            "relationship_id":
                relationship.get(
                    "relationship_id"
                ),

            "relationship":
                relationship.get(
                    "relationship"
                ),

            "target_type":
                relationship.get(
                    "target_type"
                ),

            "target_id":
                relationship.get(
                    "target_id"
                ),

            "confidence":
                relationship.get(
                    "confidence"
                ),

            "evidence":
                relationship.get(
                    "evidence",
                    {}
                )

        })

    return result


# ============================================================
# BUILD RAG TEXT
# ============================================================

def build_rag_text(
    product,
    standard_records,
    qco_records,
    regulation_records,
    product_relationships
):
    """
    Build a human-readable text representation.

    This is the text that can later be embedded
    into a vector database.
    """

    product_name = product.get(
        "product_name",
        ""
    )

    product_slug = product.get(
        "product_slug",
        ""
    )

    lines = []

    # --------------------------------------------------------
    # PRODUCT
    # --------------------------------------------------------

    lines.append(
        f"Product: {product_name}"
    )

    if product_slug:
        lines.append(
            f"Product Slug: {product_slug}"
        )

    # --------------------------------------------------------
    # STANDARDS
    # --------------------------------------------------------

    if standard_records:

        lines.append(
            "\nApplicable BIS Standards:"
        )

        for standard in standard_records:

            lines.append(
                f"- {standard.get('standard_number')}"
            )

    # --------------------------------------------------------
    # QCO
    # --------------------------------------------------------

    if qco_records:

        lines.append(
            "\nQuality Control Orders:"
        )

        for qco in qco_records:

            lines.append(
                f"- {qco.get('title')}"
            )

            if qco.get(
                "notification_number"
            ):
                lines.append(
                    "  Notification: "
                    + str(
                        qco.get(
                            "notification_number"
                        )
                    )
                )

            if qco.get(
                "effective_date"
            ):
                lines.append(
                    "  Effective Date: "
                    + str(
                        qco.get(
                            "effective_date"
                        )
                    )
                )

            if qco.get(
                "declared_standard"
            ):
                lines.append(
                    "  Declared Standard: "
                    + str(
                        qco.get(
                            "declared_standard"
                        )
                    )
                )

    # --------------------------------------------------------
    # REGULATIONS
    # --------------------------------------------------------

    if regulation_records:

        lines.append(
            "\nRegulatory Documents:"
        )

        for regulation in regulation_records:

            lines.append(
                f"- {regulation.get('document_name')}"
            )

            standards = regulation.get(
                "standards_found",
                []
            )

            if standards:

                lines.append(
                    "  Standards: "
                    + ", ".join(
                        standards
                    )
                )

    # --------------------------------------------------------
    # RELATIONSHIPS
    # --------------------------------------------------------

    if product_relationships:

        lines.append(
            "\nRegulatory Relationships:"
        )

        for relationship in product_relationships:

            relation = relationship.get(
                "relationship"
            )

            target = relationship.get(
                "target_id"
            )

            confidence = relationship.get(
                "confidence"
            )

            lines.append(
                f"- {relation} -> {target}"
                f" (confidence: {confidence})"
            )

    return "\n".join(lines)


# ============================================================
# BUILD ONE RAG RECORD
# ============================================================

def build_rag_record(
    product,
    standards,
    qcos,
    regulations,
    relationships
):
    """
    Build one complete RAG record for one product.
    """

    product_id = product.get(
        "product_id"
    )

    # --------------------------------------------------------
    # Standards
    # --------------------------------------------------------

    standard_records = get_standard_records(
        product,
        standards
    )

    # --------------------------------------------------------
    # QCOs
    # --------------------------------------------------------

    qco_records = get_qco_records(
        product,
        qcos,
        relationships
    )

    # --------------------------------------------------------
    # Regulations
    # --------------------------------------------------------

    regulation_records = (
        get_regulation_records(
            product,
            regulations,
            relationships
        )
    )

    # --------------------------------------------------------
    # Relationships
    # --------------------------------------------------------

    product_relationships = (
        get_product_relationships(
            product,
            relationships
        )
    )

    # --------------------------------------------------------
    # RAG text
    # --------------------------------------------------------

    rag_text = build_rag_text(
        product,
        standard_records,
        qco_records,
        regulation_records,
        product_relationships
    )

    # --------------------------------------------------------
    # Final record
    # --------------------------------------------------------

    return {

        "rag_id":
            f"rag_{product_id}",

        "product_id":
            product_id,

        "product_name":
            product.get(
                "product_name"
            ),

        "product_slug":
            product.get(
                "product_slug"
            ),

        "standards":
            standard_records,

        "qcos":
            qco_records,

        "regulations":
            regulation_records,

        "relationships":
            product_relationships,

        "text":
            rag_text,

        "metadata": {

            "source":
                product.get(
                    "source"
                ),

            "source_path":
                product.get(
                    "source_path"
                ),

            "standard_count":
                len(
                    standard_records
                ),

            "qco_count":
                len(
                    qco_records
                ),

            "regulation_count":
                len(
                    regulation_records
                ),

            "relationship_count":
                len(
                    product_relationships
                )

        }

    }


# ============================================================
# BUILD ALL RAG RECORDS
# ============================================================

def build_rag_records(
    products,
    standards,
    qcos,
    regulations,
    relationships
):
    """
    Build one RAG record for every discovered product.
    """

    records = []

    for product in products:

        record = build_rag_record(
            product=product,
            standards=standards,
            qcos=qcos,
            regulations=regulations,
            relationships=relationships
        )

        records.append(
            record
        )

    return records