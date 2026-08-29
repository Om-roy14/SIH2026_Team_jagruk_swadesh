import json
import hashlib

from .config import REGULATORY_DIR

from .normalizer import (
    extract_standard_numbers
)


# ============================================================
# LOAD JSON
# ============================================================

def load_json(path):

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(
                file
            )

    except Exception as e:

        print(
            f"Regulatory read error: {path}: {e}"
        )

        return None


# ============================================================
# FLATTEN JSON
# ============================================================

def flatten(value):

    if isinstance(
        value,
        str
    ):

        return value

    if isinstance(
        value,
        dict
    ):

        return " ".join(
            flatten(v)
            for v in value.values()
        )

    if isinstance(
        value,
        list
    ):

        return " ".join(
            flatten(v)
            for v in value
        )

    return ""


# ============================================================
# MAKE REGULATION ID
# ============================================================

def make_id(path):

    digest = hashlib.sha256(
        str(path).encode(
            "utf-8"
        )
    ).hexdigest()[:16]

    return (
        "reg_" +
        digest
    )


# ============================================================
# DISCOVER REGULATIONS
# ============================================================

def discover_regulations():

    records = []

    if not REGULATORY_DIR.exists():
        return records

    for path in REGULATORY_DIR.rglob(
        "*.json"
    ):

        # ----------------------------------------------------
        # QCO files are handled separately
        # ----------------------------------------------------

        try:

            path.relative_to(
                REGULATORY_DIR / "qco"
            )

            continue

        except ValueError:

            pass

        data = load_json(
            path
        )

        if not data:
            continue

        text = flatten(
            data
        )

        standards = (
            extract_standard_numbers(
                text
            )
        )

        records.append({

            "regulation_id":
                make_id(path),

            "document_name":
                path.name,

            "source":
                "BIS",

            "source_path":
                str(path),

            "standards_found":
                standards,

            "data":
                data

        })

    return records