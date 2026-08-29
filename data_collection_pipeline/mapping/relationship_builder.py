from .normalizer import (
    normalize_standard
)

from .confidence import (
    calculate_qco_confidence
)


# ============================================================
# RELATIONSHIP BUILDER
# ============================================================

def build_relationships(
    products,
    standards,
    qcos,
    regulations
):

    relationships = []

    # ========================================================
    # PRODUCT -> STANDARD
    # ========================================================

    for product in products:

        for raw_standard in product.get(
            "standards",
            []
        ):

            standard = normalize_standard(
                raw_standard
            )

            if not standard:
                continue

            standard_record = next(
                (
                    s
                    for s in standards
                    if s["standard_number"]
                    == standard
                ),
                None
            )

            if not standard_record:
                continue

            relationship_id = (
                f"{product['product_id']}"
                f"_USES_"
                f"{standard_record['standard_id']}"
            )

            relationships.append({

                "relationship_id":
                    relationship_id,

                "source_type":
                    "product",

                "source_id":
                    product["product_id"],

                "relationship":
                    "USES_STANDARD",

                "target_type":
                    "standard",

                "target_id":
                    standard_record[
                        "standard_id"
                    ],

                "confidence":
                    1.0,

                "evidence": {

                    "standard":
                        standard,

                    "source":
                        product[
                            "source_path"
                        ]

                }

            })

    # ========================================================
    # PRODUCT -> QCO
    # ========================================================

    for product in products:

        product_standards = [
            normalize_standard(x)
            for x in product.get(
                "standards",
                []
            )
        ]

        for product_standard in product_standards:

            if not product_standard:
                continue

            for qco in qcos:

                confidence, reason = (
                    calculate_qco_confidence(

                        product_standard,

                        qco.get(
                            "standards_found",
                            []
                        ),

                        product.get(
                            "product_name",
                            ""
                        ),

                        qco.get(
                            "title",
                            ""
                        )
                    )
                )

                if confidence <= 0:
                    continue

                # ------------------------------------------------
                # Safety check
                # ------------------------------------------------

                qco_id = qco.get(
                    "qco_id"
                )

                if not qco_id:
                    continue

                relationships.append({

                    "relationship_id":
                        f"{product['product_id']}"
                        f"_SUBJECT_TO_"
                        f"{qco_id}",

                    "source_type":
                        "product",

                    "source_id":
                        product["product_id"],

                    "relationship":
                        "SUBJECT_TO",

                    "target_type":
                        "qco",

                    "target_id":
                        qco_id,

                    "confidence":
                        confidence,

                    "evidence": {

                        "matched_standard":
                            product_standard,

                        "qco_standards":
                            qco.get(
                                "standards_found",
                                []
                            ),

                        "reason":
                            reason,

                        "qco_source":
                            qco.get(
                                "source_path"
                            )

                    }

                })

    # ========================================================
    # PRODUCT -> REGULATION
    # ========================================================

    for product in products:

        product_standards = [

            normalize_standard(x)

            for x in product.get(
                "standards",
                []
            )

        ]

        product_standards = [
            x
            for x in product_standards
            if x
        ]

        for regulation in regulations:

            matched = []

            for standard in regulation.get(
                "standards_found",
                []
            ):

                normalized = normalize_standard(
                    standard
                )

                if normalized in product_standards:

                    if normalized not in matched:

                        matched.append(
                            normalized
                        )

            if not matched:
                continue

            relationships.append({

                "relationship_id":
                    f"{product['product_id']}"
                    f"_REGULATED_BY_"
                    f"{regulation['regulation_id']}",

                "source_type":
                    "product",

                "source_id":
                    product["product_id"],

                "relationship":
                    "REGULATED_BY",

                "target_type":
                    "regulation",

                "target_id":
                    regulation[
                        "regulation_id"
                    ],

                "confidence":
                    0.95,

                "evidence": {

                    "matched_standards":
                        matched,

                    "source":
                        regulation[
                            "source_path"
                        ]

                }

            })

    return relationships