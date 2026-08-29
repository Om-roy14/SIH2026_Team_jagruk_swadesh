# ============================================================
# QCO MAPPER
# ============================================================
#
# Converts raw QCO JSON files into normalized QCO records.
#
# ============================================================

from pathlib import Path

import json

import re

import hashlib

from .config import (
    QCO_DIR,
    OUTPUT_DIR
)


# ============================================================
# STANDARD REGEX
# ============================================================

STANDARD_PATTERN = re.compile(
    r"\bIS\s*\d{1,6}(?::\s*\d{4})?\b",
    re.IGNORECASE
)


# ============================================================
# QCO ID
# ============================================================

def make_qco_id(path):

    digest = hashlib.sha256(
        str(path).encode("utf-8")
    ).hexdigest()[:16]

    return "qco_" + digest


# ============================================================
# LOAD JSON
# ============================================================

def load_json(path: Path):

    try:

        with path.open(
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except UnicodeDecodeError:

        try:

            with path.open(
                "r",
                encoding="utf-8-sig"
            ) as f:

                return json.load(f)

        except Exception as exc:

            print(
                f"[WARNING] Could not read: {path}"
            )

            print(
                f"         {exc}"
            )

            return None

    except json.JSONDecodeError as exc:

        print(
            f"[WARNING] Invalid JSON: {path}"
        )

        print(
            f"         {exc}"
        )

        return None

    except OSError as exc:

        print(
            f"[WARNING] Could not read: {path}"
        )

        print(
            f"         {exc}"
        )

        return None


# ============================================================
# CLEAN STRING
# ============================================================

def clean_string(value):

    if value is None:
        return None

    if isinstance(
        value,
        str
    ):

        value = value.strip()

        if not value:
            return None

        return value

    return str(value).strip() or None


# ============================================================
# NORMALIZE STANDARD
# ============================================================

def normalize_standard(value):

    if value is None:
        return None

    value = str(value).strip()

    if not value:
        return None

    match = re.search(
        r"\bIS\s*(\d{1,6})(?::\s*(\d{4}))?\b",
        value,
        re.IGNORECASE
    )

    if not match:
        return value

    number = match.group(1)

    year = match.group(2)

    if year:

        return (
            f"IS {number}:{year}"
        )

    return (
        f"IS {number}"
    )


# ============================================================
# EXTRACT STANDARDS
# ============================================================

def extract_standards_from_value(value):

    found = []

    if value is None:
        return found

    # --------------------------------------------------------
    # STRING
    # --------------------------------------------------------

    if isinstance(
        value,
        str
    ):

        matches = STANDARD_PATTERN.findall(
            value
        )

        for match in matches:

            normalized = normalize_standard(
                match
            )

            if (
                normalized
                and normalized not in found
            ):

                found.append(
                    normalized
                )

    # --------------------------------------------------------
    # LIST
    # --------------------------------------------------------

    elif isinstance(
        value,
        list
    ):

        for item in value:

            extracted = (
                extract_standards_from_value(
                    item
                )
            )

            for standard in extracted:

                if standard not in found:

                    found.append(
                        standard
                    )

    # --------------------------------------------------------
    # DICTIONARY
    # --------------------------------------------------------

    elif isinstance(
        value,
        dict
    ):

        for item in value.values():

            extracted = (
                extract_standards_from_value(
                    item
                )
            )

            for standard in extracted:

                if standard not in found:

                    found.append(
                        standard
                    )

    return found


# ============================================================
# LOOKS LIKE QCO
# ============================================================

def looks_like_qco(obj):

    if not isinstance(
        obj,
        dict
    ):

        return False

    qco_fields = {

        "title",

        "notification_number",

        "notification_date",

        "effective_date",

        "issuing_department",

        "certifying_authority",

        "scheme",

        "standard_referenced_in_original_qco"

    }

    return bool(
        qco_fields.intersection(
            obj.keys()
        )
    )


# ============================================================
# FIND QCO OBJECTS
# ============================================================

def find_qco_objects(data):

    results = []

    def add_result(obj):

        if not isinstance(
            obj,
            dict
        ):
            return

        if obj not in results:

            results.append(
                obj
            )

    def walk(node):

        # ----------------------------------------------------
        # DICTIONARY
        # ----------------------------------------------------

        if isinstance(
            node,
            dict
        ):

            # Direct qco object

            qco_value = node.get(
                "qco"
            )

            if isinstance(
                qco_value,
                dict
            ):

                add_result(
                    qco_value
                )

            elif isinstance(
                qco_value,
                list
            ):

                for item in qco_value:

                    if isinstance(
                        item,
                        dict
                    ):

                        add_result(
                            item
                        )

            # ------------------------------------------------
            # EXPLICIT QCO COLLECTIONS
            # ------------------------------------------------

            collection_keys = {

                "qcos",

                "QCOs",

                "orders",

                "quality_control_orders",

                "quality_control_orders_list"

            }

            for key in collection_keys:

                value = node.get(
                    key
                )

                if isinstance(
                    value,
                    list
                ):

                    for item in value:

                        if isinstance(
                            item,
                            dict
                        ):

                            if looks_like_qco(
                                item
                            ):

                                add_result(
                                    item
                                )

                            walk(
                                item
                            )

                        elif isinstance(
                            item,
                            list
                        ):

                            walk(
                                item
                            )

                elif isinstance(
                    value,
                    dict
                ):

                    if looks_like_qco(
                        value
                    ):

                        add_result(
                            value
                        )

                    walk(
                        value
                    )

            # ------------------------------------------------
            # RECURSIVE SEARCH
            # ------------------------------------------------

            for key, value in node.items():

                if key in {
                    "qco",
                    "qcos",
                    "QCOs",
                    "orders",
                    "quality_control_orders",
                    "quality_control_orders_list"
                }:

                    continue

                if isinstance(
                    value,
                    (
                        dict,
                        list
                    )
                ):

                    walk(
                        value
                    )

        # ----------------------------------------------------
        # LIST
        # ----------------------------------------------------

        elif isinstance(
            node,
            list
        ):

            for item in node:

                walk(
                    item
                )

    walk(
        data
    )

    return results


# ============================================================
# MAP ONE QCO
# ============================================================

def map_qco(
    qco,
    source_path,
    root_data=None
):

    # --------------------------------------------------------
    # QCO ID
    # --------------------------------------------------------

    qco_id = make_qco_id(
        source_path
    )

    # --------------------------------------------------------
    # BASIC INFORMATION
    # --------------------------------------------------------

    title = clean_string(
        qco.get(
            "title"
        )
    )

    notification_number = clean_string(
        qco.get(
            "notification_number"
        )
    )

    notification_date = clean_string(
        qco.get(
            "notification_date"
        )
    )

    effective_date = clean_string(
        qco.get(
            "effective_date"
        )
    )

    issuing_department = clean_string(
        qco.get(
            "issuing_department"
        )
    )

    certifying_authority = clean_string(
        qco.get(
            "certifying_authority"
        )
    )

    scheme = clean_string(
        qco.get(
            "scheme"
        )
    )

    # --------------------------------------------------------
    # DECLARED STANDARD
    # --------------------------------------------------------

    declared_standard = normalize_standard(
        qco.get(
            "standard_referenced_in_original_qco"
        )
    )

    # --------------------------------------------------------
    # ADDITIONAL STANDARDS
    # --------------------------------------------------------

    standards_found = []

    if declared_standard:

        standards_found.append(
            declared_standard
        )

    standard_fields = [

        "standard",

        "standards",

        "referenced_standards",

        "applicable_standards",

        "standards_referenced",

        "standard_references",

        "latest_standard",

        "latest_standard_number"

    ]

    for field in standard_fields:

        if field not in qco:
            continue

        extracted = (
            extract_standards_from_value(
                qco.get(field)
            )
        )

        for standard in extracted:

            if standard not in standards_found:

                standards_found.append(
                    standard
                )

    # --------------------------------------------------------
    # PRODUCT INFORMATION
    # --------------------------------------------------------

    product = {}

    if isinstance(
        root_data,
        dict
    ):

        raw_product = root_data.get(
            "product"
        )

        if isinstance(
            raw_product,
            dict
        ):

            product = {

                "name":
                    clean_string(
                        raw_product.get(
                            "name"
                        )
                    ),

                "standard_number":
                    normalize_standard(
                        raw_product.get(
                            "standard_number"
                        )
                    ),

                "category":
                    clean_string(
                        raw_product.get(
                            "category"
                        )
                    ),

                "description":
                    clean_string(
                        raw_product.get(
                            "description"
                        )
                    )

            }

            product = {
                key: value
                for key, value in product.items()
                if value is not None
            }

    # --------------------------------------------------------
    # FINAL RECORD
    # --------------------------------------------------------

    record = {

        "qco_id":
            qco_id,

        "title":
            title,

        "notification_number":
            notification_number,

        "notification_date":
            notification_date,

        "effective_date":
            effective_date,

        "issuing_department":
            issuing_department,

        "certifying_authority":
            certifying_authority,

        "scheme":
            scheme,

        "declared_standard":
            declared_standard,

        "standards_found":
            standards_found,

        "product":
            product,

        "source_path":
            str(source_path),

        "qco": {

            "title":
                title,

            "notification_number":
                notification_number,

            "notification_date":
                notification_date,

            "effective_date":
                effective_date,

            "issuing_department":
                issuing_department,

            "certifying_authority":
                certifying_authority,

            "scheme":
                scheme,

            "standard_referenced_in_original_qco":
                declared_standard,

            "latest_standard_clause":
                clean_string(
                    qco.get(
                        "latest_standard_clause"
                    )
                )

        }

    }

    return record


# ============================================================
# BUILD ALL QCOs
# ============================================================

def build_qcos():

    records = []

    if not QCO_DIR.exists():

        print(
            "[ERROR] QCO directory does not exist:"
        )

        print(
            QCO_DIR
        )

        return records

    json_files = sorted(
        QCO_DIR.rglob(
            "*.json"
        )
    )

    for path in json_files:

        data = load_json(
            path
        )

        if data is None:
            continue

        qco_objects = (
            find_qco_objects(
                data
            )
        )

        # ----------------------------------------------------
        # Ignore metadata/reference files
        # ----------------------------------------------------

        if not qco_objects:
            continue

        for qco in qco_objects:

            record = map_qco(
                qco=qco,
                source_path=path,
                root_data=data
            )

            # ------------------------------------------------
            # Accept only meaningful QCO records
            # ------------------------------------------------

            if (
                record["title"]
                or record["declared_standard"]
                or record["notification_number"]
            ):

                records.append(
                    record
                )

    return records


# ============================================================
# SAVE QCOs
# ============================================================

def save_qcos(
    output_path=None,
    records=None
):

    if records is None:

        records = build_qcos()

    if output_path is None:

        output_path = (
            OUTPUT_DIR /
            "qcos.json"
        )

    output_path = Path(
        output_path
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with output_path.open(
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            records,
            f,
            indent=2,
            ensure_ascii=False
        )

    return output_path


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    qcos = build_qcos()

    print(
        "=" * 70
    )

    print(
        "QCO MAPPING"
    )

    print(
        "=" * 70
    )

    print(
        f"QCO DIRECTORY : {QCO_DIR}"
    )

    print(
        f"TOTAL RECORDS : {len(qcos)}"
    )

    print()

    for index, qco in enumerate(
        qcos,
        start=1
    ):

        print(
            "-" * 70
        )

        print(
            f"RECORD #{index}"
        )

        print(
            f"QCO ID    : {qco.get('qco_id')}"
        )

        print(
            f"TITLE     : {qco.get('title')}"
        )

        print(
            f"DECLARED  : {qco.get('declared_standard')}"
        )

        print(
            f"STANDARDS : {qco.get('standards_found')}"
        )

        print(
            f"FILE      : {qco.get('source_path')}"
        )

    output = save_qcos(
        records=qcos
    )

    print()

    print(
        "=" * 70
    )

    print(
        f"OUTPUT    : {output}"
    )

    print(
        "=" * 70
    )