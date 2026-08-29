import json
import os
import re


def save_json(path, data):

    os.makedirs(
        os.path.dirname(path),
        exist_ok=True
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def sanitize_name(name):

    if not name:
        return "unknown"

    name = str(name).strip()

    # Replace Windows-invalid characters
    name = re.sub(
        r'[<>:"/\\|?*]',
        '',
        name
    )

    # Replace whitespace sequences
    name = re.sub(
        r'\s+',
        '_',
        name
    )

    # Remove repeated underscores
    name = re.sub(
        r'_+',
        '_',
        name
    )

    # Keep names manageable
    name = name[:150]

    return name.strip(
        "._"
    ).lower()


def create_standard_directory(
    base_directory,
    standard_number,
    standard_name
):

    product_name = sanitize_name(
        standard_name
    )

    standard_name_clean = sanitize_name(
        standard_number
    )

    product_dir = os.path.join(
        base_directory,
        product_name
    )

    standard_dir = os.path.join(
        product_dir,
        "standards",
        standard_name_clean
    )

    documents_dir = os.path.join(
        standard_dir,
        "documents"
    )

    os.makedirs(
        documents_dir,
        exist_ok=True
    )

    return {
        "product_dir": product_dir,
        "standard_dir": standard_dir,
        "documents_dir": documents_dir,
        "product_name": product_name,
        "standard_name": standard_name_clean
    }