from .normalizer import normalize_standard


# ============================================================
# BUILD STANDARDS
# ============================================================

def build_standards(products):

    standards = {}

    for product in products:

        for raw_standard in product.get(
            "standards",
            []
        ):

            standard_number = normalize_standard(
                raw_standard
            )

            if not standard_number:
                continue

            # ------------------------------------------------
            # CREATE STANDARD
            # ------------------------------------------------

            if standard_number not in standards:

                standards[standard_number] = {

                    "standard_id":
                        "standard_"
                        + standard_number
                        .replace(" ", "_")
                        .replace(":", "_"),

                    "standard_number":
                        standard_number,

                    "products": []

                }

            # ------------------------------------------------
            # CONNECT PRODUCT TO STANDARD
            # ------------------------------------------------

            if product["product_id"] not in standards[
                standard_number
            ]["products"]:

                standards[
                    standard_number
                ]["products"].append(
                    product["product_id"]
                )

    return list(
        standards.values()
    )