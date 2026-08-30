from pathlib import Path
from .product_loader import (
    discover_products
)

from .standard_mapper import (
    build_standards
)

from .qco_mapper import (
    build_qcos
)

from .regulatory_mapper import (
    discover_regulations
)

from .relationship_builder import (
    build_relationships
)

from .exporter import (
    save_json,
    build_rag_records
)


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "=" * 70
    )

    print(
        "BIS PRODUCT MAPPING ENGINE"
    )

    print(
        "=" * 70
    )

    # ========================================================
    # PRODUCTS
    # ========================================================

    print(
        "\n[1] Loading products..."
    )

    products = discover_products()

    print(
        f"Products discovered: "
        f"{len(products)}"
    )

    # ========================================================
    # STANDARDS
    # ========================================================

    print(
        "\n[2] Building standards..."
    )

    standards = build_standards(
        products
    )

    print(
        f"Standards discovered: "
        f"{len(standards)}"
    )

    # ========================================================
    # QCO
    # ========================================================

    print(
        "\n[3] Loading QCO data..."
    )

    qcos = build_qcos()

    print(
        f"QCO records discovered: "
        f"{len(qcos)}"
    )

    # ========================================================
    # REGULATORY
    # ========================================================

    print(
        "\n[4] Loading regulatory data..."
    )

    regulations = (
        discover_regulations()
    )

    print(
        f"Regulatory records: "
        f"{len(regulations)}"
    )

    # ========================================================
    # RELATIONSHIPS
    # ========================================================

    print(
        "\n[5] Building relationships..."
    )

    relationships = build_relationships(

        products,

        standards,

        qcos,

        regulations

    )

    print(
        f"Relationships created: "
        f"{len(relationships)}"
    )

    # ========================================================
    # RAG RECORDS
    # ========================================================

    print(
        "\n[6] Building RAG-ready records..."
    )

    rag_records = build_rag_records(

        products,

        standards,

        qcos,

        regulations,

        relationships

    )

    print(
        f"RAG records created: "
        f"{len(rag_records)}"
    )

    # ========================================================
    # EXPORT
    # ========================================================

    print(
        "\n[7] Exporting..."
    )

    output_dir = Path("data") / "mapped"

    save_json(
        products,
        output_dir / "products.json"
    )

    save_json(
        standards,
        output_dir / "standards.json"
    )

    save_json(
        qcos,
        output_dir / "qcos.json"
    )

    save_json(
        regulations,
        output_dir / "regulations.json"
    )

    save_json(
        relationships,
        output_dir / "relationships.json"
    )

    save_json(
        rag_records,
        output_dir / "rag_records.json"
    )

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print(
        "\n" + "=" * 70
    )

    print(
        "MAPPING COMPLETED"
    )

    print(
        "=" * 70
    )

    print(
        f"\nProducts      : "
        f"{len(products)}"
    )

    print(
        f"Standards      : "
        f"{len(standards)}"
    )

    print(
        f"QCOs          : "
        f"{len(qcos)}"
    )

    print(
        f"Regulations    : "
        f"{len(regulations)}"
    )

    print(
        f"Relationships  : "
        f"{len(relationships)}"
    )

    print(
        f"RAG records    : "
        f"{len(rag_records)}"
    )

    print(
        "\nOutput:"
    )

    print(
        "data/mapped/"
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()