import os
import re
import json


# ============================================================
# PRODUCT CATEGORY
# ============================================================

def derive_product_category(
    standard_name
):

    if not standard_name:

        return "unknown_product"

    name = standard_name.strip()

    # --------------------------------------------------------
    # Remove revision information
    # --------------------------------------------------------

    name = re.sub(
        r"\s*\([^)]*revision[^)]*\)",
        "",
        name,
        flags=re.IGNORECASE
    )

    # --------------------------------------------------------
    # Remove amendment information
    # --------------------------------------------------------

    name = re.sub(
        r"\s*[-–:]?\s*"
        r"(amendment|amdt)"
        r"\s*(no\.?)?\s*\d+.*$",
        "",
        name,
        flags=re.IGNORECASE
    )

    # --------------------------------------------------------
    # Remove common description suffixes
    # --------------------------------------------------------

    suffixes = [

        r"\s*[-–]\s*SPECIFICATION.*$",

        r"\s*[-–]\s*REQUIREMENTS.*$",

        r"\s*[-–]\s*METHOD OF TEST.*$",

        r"\s*[-–]\s*CODE OF PRACTICE.*$",

        r"\s*[-–]\s*GUIDELINES.*$",

        r"\s*[-–]\s*GENERAL REQUIREMENTS.*$",
    ]

    for pattern in suffixes:

        name = re.sub(
            pattern,
            "",
            name,
            flags=re.IGNORECASE
        )

    # --------------------------------------------------------
    # Normalize whitespace
    # --------------------------------------------------------

    name = re.sub(
        r"\s+",
        " ",
        name
    )

    name = name.strip(
        " -–:,"
    )

    if not name:

        return "unknown_product"

    # --------------------------------------------------------
    # Folder-safe name
    # --------------------------------------------------------

    category = name.lower()

    category = re.sub(
        r"[^a-z0-9]+",
        "_",
        category
    )

    category = category.strip(
        "_"
    )

    return (
        category
        or "unknown_product"
    )


# ============================================================
# STANDARD FILE NAME
# ============================================================

def standard_filename(
    standard_number
):

    value = standard_number.lower()

    value = re.sub(
        r"[^a-z0-9]+",
        "_",
        value
    )

    return value.strip(
        "_"
    )


# ============================================================
# LOAD JSON
# ============================================================

def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# ============================================================
# SAVE JSON
# ============================================================

def save_json(
    path,
    data
):

    os.makedirs(
        os.path.dirname(path),
        exist_ok=True
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


# ============================================================
# ORGANIZE ONE STANDARD
# ============================================================

def organize_standard(
    standard_directory
):

    complete_path = os.path.join(
        standard_directory,
        "complete.json"
    )

    if not os.path.exists(
        complete_path
    ):

        print(
            "complete.json not found:"
        )

        print(
            complete_path
        )

        return None

    complete_data = load_json(
        complete_path
    )

    standard = complete_data.get(
        "standard",
        {}
    )

    standard_name = standard.get(
        "standardName",
        ""
    )

    standard_number = standard.get(
        "standardNumber",
        "unknown_standard"
    )

    # --------------------------------------------------------
    # DERIVE PRODUCT
    # --------------------------------------------------------

    product_category = derive_product_category(
        standard_name
    )

    print(
        f"\nProduct: {product_category}"
    )

    # --------------------------------------------------------
    # PRODUCT DIRECTORY
    # --------------------------------------------------------

    product_dir = os.path.join(
        "data",
        "products",
        product_category
    )

    os.makedirs(
        product_dir,
        exist_ok=True
    )

    # --------------------------------------------------------
    # STANDARDS DIRECTORY
    # --------------------------------------------------------

    standards_dir = os.path.join(
        product_dir,
        "standards"
    )

    os.makedirs(
        standards_dir,
        exist_ok=True
    )

    # --------------------------------------------------------
    # STANDARD JSON
    # --------------------------------------------------------

    filename = (
        standard_filename(
            standard_number
        )
        + ".json"
    )

    standard_path = os.path.join(
        standards_dir,
        filename
    )

    save_json(
        standard_path,
        complete_data
    )

    # --------------------------------------------------------
    # DOCUMENT LOCATION
    # --------------------------------------------------------

    document_directory = os.path.join(
        "data",
        "documents",
        product_category,
        standard_filename(
            standard_number
        )
    )

    os.makedirs(
        document_directory,
        exist_ok=True
    )

    # --------------------------------------------------------
    # PRODUCT METADATA
    # --------------------------------------------------------

    product_json = os.path.join(
        product_dir,
        "product.json"
    )

    # Preserve existing product data
    # if product already exists.

    if os.path.exists(
        product_json
    ):

        product_data = load_json(
            product_json
        )

    else:

        product_data = {
            "product_category": product_category,
            "product_name": standard_name,
            "standards": []
        }

    # --------------------------------------------------------
    # Add standard
    # --------------------------------------------------------

    standards = product_data.setdefault(
        "standards",
        []
    )

    if standard_number not in standards:

        standards.append(
            standard_number
        )

    product_data[
        "product_name"
    ] = product_category.replace(
        "_",
        " "
    ).title()

    save_json(
        product_json,
        product_data
    )

    # --------------------------------------------------------
    # Document reference
    # --------------------------------------------------------

    document_reference_path = os.path.join(
        standard_path
    )

    return {
        "product_category": product_category,
        "product_directory": product_dir,
        "standard_json": standard_path,
        "document_directory": document_directory
    }


# ============================================================
# ORGANIZE EVERYTHING
# ============================================================

def organize_all():

    raw_directory = "data/raw"

    if not os.path.exists(
        raw_directory
    ):

        print(
            "data/raw does not exist."
        )

        return

    print(
        "\nOrganizing collected standards..."
    )

    for folder in os.listdir(
        raw_directory
    ):

        standard_directory = os.path.join(
            raw_directory,
            folder
        )

        if not os.path.isdir(
            standard_directory
        ):

            continue

        result = organize_standard(
            standard_directory
        )

        if result:

            print(
                "✓ "
                + result[
                    "product_category"
                ]
            )


if __name__ == "__main__":

    organize_all()