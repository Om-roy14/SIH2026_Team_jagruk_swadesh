import os
from urllib.parse import urlparse, parse_qs

from scraper.browser import discover_apis
from scraper.api import collect_endpoint
from scraper.storage import save_json, create_standard_directory

# FIXED: Corrected import path for the downloader module
from scraper.downloader import download_documents

# ============================================================
# EXTRACT ENCRYPTED ID
# ============================================================
def extract_encrypted_id(url):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    values = params.get("encryptedId")
    if not values:
        return None
    return values[0]

# ============================================================
# FIND STANDARD DETAILS
# ============================================================
def find_standard_details(api_results):
    for result in api_results:
        if result.get("endpoint") != "getWebsiteStandardDetails":
            continue
        records = result.get("records", [])
        if not records:
            continue
        for record in records:
            if not isinstance(record, dict):
                continue
            if "standardName" in record:
                return record
            for key in ("data", "result", "responseData", "standard", "standardDetails"):
                nested = record.get(key)
                if not isinstance(nested, dict):
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

    encrypted_id = extract_encrypted_id(url)
    if encrypted_id:
        print("\nEncrypted ID detected.")
    else:
        print("\nWarning: encryptedId was not found.")

    api_requests = discover_apis(url)
    print(f"\nDiscovered {len(api_requests)} relevant APIs.")
    if not api_requests:
        raise RuntimeError("No BIS data APIs were discovered.")
    for api in api_requests:
        print(f"  ✓ {api['endpoint']}")

    results = []
    for api in api_requests:
        endpoint = api["endpoint"]
        print(f"\nCollecting: {endpoint}")
        try:
            result = collect_endpoint(api)
            results.append(result)
        except Exception as e:
            print(f"  ✗ Failed: {e}")
            results.append({
                "endpoint": endpoint,
                "url": api.get("url", ""),
                "records": [],
                "error": str(e)
            })

    standard = find_standard_details(results)
    if not standard:
        raise RuntimeError("BIS standard information could not be extracted.")

    standard_number = standard.get("standardNumber") or "unknown_standard"
    standard_name = standard.get("standardName") or "unknown_product"

    print("\nStandard:")
    print(f"  Number: {standard_number}")
    print(f"  Name  : {standard_name}")

    directories = create_standard_directory("data/products", standard_number, standard_name)
    product_dir = directories["product_dir"]
    standard_dir = directories["standard_dir"]
    documents_dir = directories["documents_dir"]
    product_slug = directories["product_name"]

    product_data = {
        "product_name": standard_name,
        "product_slug": product_slug,
        "source": "BIS",
        "standards": [standard_number]
    }
    save_json(os.path.join(product_dir, "product.json"), product_data)

    save_json(os.path.join(standard_dir, "standard.json"), {
        "source_url": url,
        "encrypted_id": encrypted_id,
        "standard": standard
    })

    complete_sections = {}
    for result in results:
        endpoint = result.get("endpoint", "unknown_endpoint")
        
        # FIXED: Inject Standard Number and Product Name into raw records
        if endpoint in ["getStandardLaboratoryDetails", "getStandardLicenseDetails"]:
            for record in result.get("records", []):
                if isinstance(record, dict):
                    if "standardNumber" not in record:
                        record["standardNumber"] = standard_number
                    if "productName" not in record:
                        record["productName"] = standard_name

        filename = endpoint.lower() + ".json"
        path = os.path.join(standard_dir, filename)
        save_json(path, result)

        complete_sections[endpoint] = {
            "url": result.get("url", ""),
            "records": result.get("records", []),
            "error": result.get("error")
        }

    complete_data = {
        "source_url": url,
        "encrypted_id": encrypted_id,
        "standard": standard,
        "sections": complete_sections
    }
    complete_path = os.path.join(standard_dir, "complete.json")
    save_json(complete_path, complete_data)

    print("\n" + "-" * 70)
    print("DOCUMENT COLLECTION")
    print("-" * 70)
    try:
        # FIXED: Pass correct variables (json path and output directory) to downloader
        download_documents(complete_path, documents_dir)
    except Exception as e:
        print("\nDocument download warning:")
        print(f"  {e}")

    print("\n" + "=" * 70)
    print("COLLECTION COMPLETED")
    print("=" * 70)
    return complete_data