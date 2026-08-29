# regulatory/sources.py

BIS_BASE = "https://www.bis.gov.in"


SOURCES = {

    # ---------------------------------------------------------
    # QCO
    # ---------------------------------------------------------

    "qco_main": (
        f"{BIS_BASE}/product-certification/"
        "products-under-compulsory-certification/"
        "?lang=en"
    ),

    "qco_upcoming": (
        f"{BIS_BASE}/upcoming-qcos-notified-and-due-for-implementation/"
        "?lang=en"
    ),

    "qco_scheme_1": (
        f"{BIS_BASE}/product-certification/"
        "products-under-compulsory-certification/"
        "scheme-i-mark-scheme/?lang=en"
    ),

    "qco_guidance": (
        f"{BIS_BASE}/branch_important_lin/"
        "guidance-document-on-quality-control-orders-qcos/"
        "?lang=en"
    ),

    # ---------------------------------------------------------
    # BIS LEGAL FRAMEWORK
    # ---------------------------------------------------------

    "bis_act_rules_regulations": (
        f"{BIS_BASE}/the-bureau/"
        "bis-act-rules-and-regulations/"
        "?lang=en"
    ),

    # ---------------------------------------------------------
    # CERTIFICATION
    # ---------------------------------------------------------

    "certification_process": (
        f"{BIS_BASE}/product-certification/"
        "product-certification-process/"
        "?lang=en"
    ),

    "product_certification": (
        f"{BIS_BASE}/product-certification/"
        "?lang=en"
    ),

    "certification_faq": (
        f"{BIS_BASE}/product-certification/"
        "product-certification-faq/"
        "?lang=en"
    ),

    # ---------------------------------------------------------
    # PRODUCT MANUAL ARCHIVE
    # ---------------------------------------------------------

    "product_manual_archive": (
        f"{BIS_BASE}/product-manual-archive/"
        "?lang=en"
    ),

    # ---------------------------------------------------------
    # OLD CERTIFICATION GUIDELINES
    # ---------------------------------------------------------

    "certification_archive": (
        f"{BIS_BASE}/product-certification/"
        "product-certification-process-archives/"
        "?lang=en"
    ),
}