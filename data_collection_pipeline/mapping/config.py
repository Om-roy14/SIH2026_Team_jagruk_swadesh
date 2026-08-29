from pathlib import Path


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# DATA DIRECTORIES
# ============================================================

DATA_DIR = BASE_DIR / "data"

PRODUCTS_DIR = DATA_DIR / "products"

RAW_DIR = DATA_DIR / "raw"

QCO_DIR = RAW_DIR / "regulatory" / "qco"

REGULATORY_DIR = RAW_DIR / "regulatory"

OUTPUT_DIR = DATA_DIR / "mapped"


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)