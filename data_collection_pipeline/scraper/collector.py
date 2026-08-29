import os
from urllib.parse import urlparse, parse_qs

from scraper.browser import discover_apis
from scraper.api import collect_endpoint
from scraper.storage import (
    save_json,
    create_standard_directory
)

from download_documents import download_documents


# ============================================================
# EXTRACT ENCRYPTED ID
# ============================================================

def extract_encrypted_id(url):

    parsed = urlparse(url)

    params = parse_qs(
        parsed.query
    )

    values = params.get(
        "encryptedId"
    )

    if not values:
        return None

    return values[0]


# ============================================================
# FIND STANDARD DETAILS
# ============================================================

def find_standard_details(api_results):

    for result in api_results:

        if (
            result.get("endpoint")
            != "getWebsiteStandardDetails"
        ):
            continue

        records = result.get(
            "records",
            []
        )

        if not records:
            continue

        for record in records:

            if not isinstance(
                record,
                dict
            ):
                continue

            # ----------------------------------------------
            # Direct response
            # ----------------------------------------------

            if "standardName" in record:

                return record

            # ----------------------------------------------
            # Wrapped response
            # ----------------------------------------------

            for key in (
                "data",
                "result",
                "responseData",
                "standard",
                "standardDetails"
            ):

                nested = record.get(
                    key
                )

                if not isinstance(
                    nested,
                    dict
                ):
                    continue

                if "standardName" in nested:

                    return nested

    return {}


# ============================================================
# COLLECT BIS STANDARD
# ============================================================

def collect_bis_page(url):

    print("=" * 70)
    print("BIS COMPLETE DATA PIPELINE")
    print("=" * 70)

    print("\nInput URL:")
    print(url)

    # ========================================================
    # STEP 1 — ENCRYPTED ID
    # ========================================================

    encrypted_id = extract_encrypted_id(
        url
    )

    if encrypted_id:

        print(
            "\nEncrypted ID detected."
        )

    else:

        print(
            "\nWarning: encryptedId was not found."
        )

    # ========================================================
    # STEP 2 — DISCOVER BIS APIs
    # ========================================================

    api_requests = discover_apis(
        url
    )

    print(
        f"\nDiscovered "
        f"{len(api_requests)} relevant APIs."
    )

    if not api_requests:

        raise RuntimeError(
            "No BIS data APIs were discovered."
        )

    for api in api_requests:

        print(
            f"  ✓ {api['endpoint']}"
        )

    # ========================================================
    # STEP 3 — COLLECT API DATA
    # ========================================================

    results = []

    for api in api_requests:

        endpoint = api[
            "endpoint"
        ]

        print(
            f"\nCollecting: "
            f"{endpoint}"
        )

        try:

            result = collect_endpoint(
                api
            )

            results.append(
                result
            )

        except Exception as e:

            print(
                f"  ✗ Failed: {e}"
            )

            results.append(
                {
                    "endpoint": endpoint,
                    "url": api.get(
                        "url",
                        ""
                    ),
                    "records": [],
                    "error": str(e)
                }
            )

    # ========================================================
    # STEP 4 — FIND STANDARD INFORMATION
    # ========================================================

    standard = find_standard_details(
        results
    )

    if not standard:

        raise RuntimeError(
            "BIS standard information could not "
            "be extracted from "
            "getWebsiteStandardDetails."
        )

    standard_number = (
        standard.get(
            "standardNumber"
        )
        or "unknown_standard"
    )

    standard_name = (
        standard.get(
            "standardName"
        )
        or "unknown_product"
    )

    print("\nStandard:")
    print(
        f"  Number: {standard_number}"
    )

    print(
        f"  Name  : {standard_name}"
    )

    # ========================================================
    # STEP 5 — CREATE PRODUCT / STANDARD STRUCTURE
    # ========================================================

    directories = create_standard_directory(
        "data/products",
        standard_number,
        standard_name
    )

    product_dir = directories[
        "product_dir"
    ]

    standard_dir = directories[
        "standard_dir"
    ]

    documents_dir = directories[
        "documents_dir"
    ]

    # ========================================================
    # STEP 6 — SAVE PRODUCT METADATA
    # ========================================================

    product_slug = directories[
        "product_name"
    ]

    product_data = {

        "product_name": standard_name,

        "product_slug": product_slug,

        "source": "BIS",

        "standards": [
            standard_number
        ]
    }

    product_json = os.path.join(
        product_dir,
        "product.json"
    )

    save_json(
        product_json,
        product_data
    )

    # ========================================================
    # STEP 7 — SAVE STANDARD METADATA
    # ========================================================

    standard_json = os.path.join(
        standard_dir,
        "standard.json"
    )

    save_json(
        standard_json,
        {
            "source_url": url,
            "encrypted_id": encrypted_id,
            "standard": standard
        }
    )

    # ========================================================
    # STEP 8 — SAVE EACH API SECTION
    # ========================================================

    complete_sections = {}

    for result in results:

        endpoint = result.get(
            "endpoint",
            "unknown_endpoint"
        )

        filename = (
            endpoint.lower()
            + ".json"
        )

        path = os.path.join(
            standard_dir,
            filename
        )

        save_json(
            path,
            result
        )

        complete_sections[
            endpoint
        ] = {

            "url": result.get(
                "url",
                ""
            ),

            "records": result.get(
                "records",
                []
            ),

            "error": result.get(
                "error"
            )
        }

    # ========================================================
    # STEP 9 — CREATE COMPLETE JSON
    # ========================================================

    complete_data = {

        "source_url": url,

        "encrypted_id": encrypted_id,

        "standard": standard,

        "sections": complete_sections
    }

    complete_path = os.path.join(
        standard_dir,
        "complete.json"
    )

    save_json(
        complete_path,
        complete_data
    )

    # ========================================================
    # STEP 10 — DOWNLOAD DOCUMENTS
    # ========================================================

    print("\n" + "-" * 70)
    print("DOCUMENT COLLECTION")
    print("-" * 70)

    try:

        download_documents(
            standard_dir,
            standard_number
        )

    except Exception as e:

        print(
            "\nDocument download warning:"
        )

        print(
            f"  {e}"
        )

    # ========================================================
    # STEP 11 — FINAL OUTPUT
    # ========================================================

    print("\n" + "=" * 70)
    print("COLLECTION COMPLETED")
    print("=" * 70)

    print("\nProduct:")
    print(
        product_dir
    )

    print("\nStandard:")
    print(
        standard_dir
    )

    print("\nDocuments:")
    print(
        documents_dir
    )

    print("\nComplete dataset:")
    print(
        complete_path
    )

    print("\nAPI sections saved:")

    for result in results:

        print(
            f"  ✓ "
            f"{result.get('endpoint')}"
        )

    print("\n" + "=" * 70)

    return complete_data