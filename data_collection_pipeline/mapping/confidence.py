from .normalizer import normalize_standard


# ============================================================
# QCO CONFIDENCE
# ============================================================

def calculate_qco_confidence(
    product_standard,
    qco_standards,
    product_name="",
    qco_title=""
):
    """
    Calculate confidence between a product and QCO.

    Returns:

        (confidence, reason)
    """

    product_standard = normalize_standard(
        product_standard
    )

    if not product_standard:
        return 0.0, "No product standard"

    normalized_qco_standards = []

    for standard in qco_standards:

        normalized = normalize_standard(
            standard
        )

        if normalized:
            normalized_qco_standards.append(
                normalized
            )

    # --------------------------------------------------------
    # Exact standard match
    # --------------------------------------------------------

    if product_standard in normalized_qco_standards:

        return (
            1.0,
            "Exact standard match"
        )

    # --------------------------------------------------------
    # Product/QCO title match
    # --------------------------------------------------------

    product_text = (
        str(product_name)
        .lower()
        .strip()
    )

    qco_text = (
        str(qco_title)
        .lower()
        .strip()
    )

    if (
        product_text
        and qco_text
        and product_text in qco_text
    ):

        return (
            0.75,
            "Product name appears in QCO title"
        )

    # --------------------------------------------------------
    # No relationship
    # --------------------------------------------------------

    return (
        0.0,
        "No standard or product-name match"
    )