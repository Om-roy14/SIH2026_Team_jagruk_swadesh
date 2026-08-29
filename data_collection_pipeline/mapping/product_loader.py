import json

from .config import PRODUCTS_DIR


def load_json(path):

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception as e:

        print(
            f"ERROR reading {path}: {e}"
        )

        return None


def discover_products():

    products = []

    if not PRODUCTS_DIR.exists():
        return products

    for product_dir in PRODUCTS_DIR.iterdir():

        if not product_dir.is_dir():
            continue

        product_file = (
            product_dir /
            "product.json"
        )

        if not product_file.exists():
            continue

        data = load_json(product_file)

        if not isinstance(data, dict):
            continue

        product_name = data.get(
            "product_name",
            product_dir.name
        )

        product_slug = data.get(
            "product_slug",
            product_dir.name
        )

        standards = data.get(
            "standards",
            []
        )

        product_id = (
            "product_" +
            product_slug.lower()
        )

        products.append({

            "product_id": product_id,

            "product_name": product_name,

            "product_slug": product_slug,

            "source": data.get(
                "source",
                "BIS"
            ),

            "standards": standards,

            "source_path":
                str(product_file)

        })

    return products