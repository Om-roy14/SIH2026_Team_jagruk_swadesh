import json
import hashlib
from pathlib import Path

from .config import QCO_DIR, OUTPUT_DIR
# FIXED: Import normalization logic instead of duplicating it
from .normalizer import normalize_standard, extract_standard_numbers

# ============================================================
# QCO ID
# ============================================================
def make_qco_id(path):
    digest = hashlib.sha256(str(path).encode("utf-8")).hexdigest()[:16]
    return "qco_" + digest

# ============================================================
# LOAD JSON
# ============================================================
def load_json(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        print(f"[WARNING] Could not read JSON: {path} - {exc}")
        return None

def clean_string(value):
    if value is None: return None
    if isinstance(value, str):
        val = value.strip()
        return val if val else None
    return str(value).strip() or None

# ============================================================
# EXTRACT STANDARDS (Recursive)
# ============================================================
def extract_standards_from_value(value):
    found = []
    if value is None: return found

    if isinstance(value, str):
        standards = extract_standard_numbers(value)
        for std in standards:
            if std not in found:
                found.append(std)
                
    elif isinstance(value, list):
        for item in value:
            for standard in extract_standards_from_value(item):
                if standard not in found: found.append(standard)
                
    elif isinstance(value, dict):
        for item in value.values():
            for standard in extract_standards_from_value(item):
                if standard not in found: found.append(standard)
                
    return found

# ============================================================
# LOOKS LIKE QCO
# ============================================================
def looks_like_qco(obj):
    if not isinstance(obj, dict): return False
    qco_fields = {
        "title", "notification_number", "notification_date",
        "effective_date", "issuing_department", "certifying_authority",
        "scheme", "standard_referenced_in_original_qco"
    }
    return bool(qco_fields.intersection(obj.keys()))

# ============================================================
# FIND QCO OBJECTS
# ============================================================
def find_qco_objects(data):
    results = []

    def add_result(obj):
        if isinstance(obj, dict) and obj not in results:
            results.append(obj)

    def walk(node):
        if isinstance(node, dict):
            qco_value = node.get("qco")
            if isinstance(qco_value, dict):
                add_result(qco_value)
            elif isinstance(qco_value, list):
                for item in qco_value: add_result(item)

            collection_keys = {"qcos", "QCOs", "orders", "quality_control_orders", "quality_control_orders_list"}
            for key in collection_keys:
                val = node.get(key)
                if isinstance(val, list):
                    for item in val:
                        if looks_like_qco(item): add_result(item)
                        walk(item)
                elif isinstance(val, dict):
                    if looks_like_qco(val): add_result(val)
                    walk(val)

            for key, val in node.items():
                if key not in collection_keys.union({"qco"}):
                    if isinstance(val, (dict, list)): walk(val)
                    
        elif isinstance(node, list):
            for item in node: walk(item)

    walk(data)
    return results

# ============================================================
# MAP ONE QCO
# ============================================================
def map_qco(qco, source_path, root_data=None):
    qco_id = make_qco_id(source_path)
    title = clean_string(qco.get("title"))
    notification_number = clean_string(qco.get("notification_number"))
    notification_date = clean_string(qco.get("notification_date"))
    effective_date = clean_string(qco.get("effective_date"))
    issuing_department = clean_string(qco.get("issuing_department"))
    certifying_authority = clean_string(qco.get("certifying_authority"))
    scheme = clean_string(qco.get("scheme"))
    
    declared_standard = normalize_standard(qco.get("standard_referenced_in_original_qco"))

    standards_found = []
    if declared_standard:
        standards_found.append(declared_standard)

    standard_fields = [
        "standard", "standards", "referenced_standards", "applicable_standards",
        "standards_referenced", "standard_references", "latest_standard", "latest_standard_number"
    ]

    for field in standard_fields:
        if field in qco:
            extracted = extract_standards_from_value(qco.get(field))
            for standard in extracted:
                if standard not in standards_found:
                    standards_found.append(standard)

    product = {}
    if isinstance(root_data, dict) and isinstance(root_data.get("product"), dict):
        raw_product = root_data.get("product")
        product = {
            "name": clean_string(raw_product.get("name")),
            "standard_number": normalize_standard(raw_product.get("standard_number")),
            "category": clean_string(raw_product.get("category")),
            "description": clean_string(raw_product.get("description"))
        }
        product = {k: v for k, v in product.items() if v is not None}

    return {
        "qco_id": qco_id,
        "title": title,
        "notification_number": notification_number,
        "notification_date": notification_date,
        "effective_date": effective_date,
        "issuing_department": issuing_department,
        "certifying_authority": certifying_authority,
        "scheme": scheme,
        "declared_standard": declared_standard,
        "standards_found": standards_found,
        "product": product,
        "source_path": str(source_path),
        "qco": {
            "title": title,
            "notification_number": notification_number,
            "notification_date": notification_date,
            "effective_date": effective_date,
            "issuing_department": issuing_department,
            "certifying_authority": certifying_authority,
            "scheme": scheme,
            "standard_referenced_in_original_qco": declared_standard,
            "latest_standard_clause": clean_string(qco.get("latest_standard_clause"))
        }
    }

# ============================================================
# BUILD ALL QCOs
# ============================================================
def build_qcos():
    records = []
    if not QCO_DIR.exists():
        return records

    json_files = sorted(QCO_DIR.rglob("*.json"))
    for path in json_files:
        data = load_json(path)
        if not data: continue

        qco_objects = find_qco_objects(data)
        if not qco_objects: continue

        for qco in qco_objects:
            record = map_qco(qco=qco, source_path=path, root_data=data)
            if record["title"] or record["declared_standard"] or record["notification_number"]:
                records.append(record)
    return records

# ============================================================
# SAVE QCOs
# ============================================================
def save_qcos(output_path=None, records=None):
    if records is None: records = build_qcos()
    if output_path is None: output_path = OUTPUT_DIR / "qcos.json"

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    return output_path

if __name__ == "__main__":
    qcos = build_qcos()
    print("=" * 70)
    print("QCO MAPPING")
    print("=" * 70)
    output = save_qcos(records=qcos)
    print(f"OUTPUT    : {output}")