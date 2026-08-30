# ============================================================
# BUILD RAG TEXT (Update this function in exporter.py)
# ============================================================
import json
from pathlib import Path
def save_json(data, path):
    """Safely saves data to a JSON file, handling strings, paths, or lists of parts."""
    if isinstance(path, (list, tuple)):
        file_path = Path(*path)
    else:
        file_path = Path(path)
        
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def build_rag_records(products_data, standards_data, qcos_data, regulations_data, relationships_data):
    """
    Builds the complete list of structured RAG records for all products.
    """
    records = []
    
    # Map products by their identifier for quick lookup
    for product in products_data:
        p_id = product.get("id") or product.get("product_id")
        p_name = product.get("product_name", "")
        
        # Gather related data for this product
        p_standards = [s for s in standards_data if s.get("product_id") == p_id or s.get("product_name") == p_name]
        p_qcos = [q for q in qcos_data if q.get("product_id") == p_id]
        p_regs = [r for r in regulations_data if r.get("product_id") == p_id]
        p_rels = [rel for rel in relationships_data if rel.get("source_id") == p_id]
        
        text_content = build_rag_text(
            product=product,
            standard_records=p_standards,
            qco_records=p_qcos,
            regulation_records=p_regs,
            product_relationships=p_rels
        )
        
        records.append({
            "product_name": p_name,
            "product_slug": product.get("product_slug", ""),
            "text": text_content
        })
        
    return records


def build_rag_text(
    product,
    standard_records,
    qco_records,
    regulation_records,
    product_relationships
):
    """
    Build a human-readable text representation.
    """
    product_name = product.get("product_name", "")
    product_slug = product.get("product_slug", "")
    lines = []

    lines.append(f"Product: {product_name}")
    if product_slug:
        lines.append(f"Product Slug: {product_slug}")

    if standard_records:
        lines.append("\nApplicable BIS Standards:")
        for standard in standard_records:
            lines.append(f"- {standard.get('standard_number')}")

    if qco_records:
        lines.append("\nQuality Control Orders:")
        for qco in qco_records:
            lines.append(f"- {qco.get('title')}")
            if qco.get("notification_number"):
                lines.append("  Notification: " + str(qco.get("notification_number")))
            if qco.get("effective_date"):
                lines.append("  Effective Date: " + str(qco.get("effective_date")))
            if qco.get("declared_standard"):
                lines.append("  Declared Standard: " + str(qco.get("declared_standard")))

    if regulation_records:
        lines.append("\nRegulatory Documents:")
        for regulation in regulation_records:
            lines.append(f"- {regulation.get('document_name')}")
            standards = regulation.get("standards_found", [])
            
            if standards:
                # FIXED: Prevent massive lists of standards from polluting the RAG text
                if len(standards) > 5:
                    displayed_stds = ", ".join(standards[:5])
                    lines.append(f"  Standards: {displayed_stds} (+ {len(standards) - 5} others)")
                else:
                    lines.append("  Standards: " + ", ".join(standards))

    if product_relationships:
        lines.append("\nRegulatory Relationships:")
        for relationship in product_relationships:
            relation = relationship.get("relationship")
            target = relationship.get("target_id")
            confidence = relationship.get("confidence")
            lines.append(f"- {relation} -> {target} (confidence: {confidence})")

    return "\n".join(lines)