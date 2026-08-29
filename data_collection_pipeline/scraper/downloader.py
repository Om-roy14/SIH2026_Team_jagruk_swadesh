import os
import json
import requests
from urllib.parse import urljoin


# BIS document servers discovered from the BIS APIs
BIS_DOCUMENT_BASE_URLS = [
    "https://standards.bis.gov.in/",
    "https://standardsadmin.bis.gov.in/",
]


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_document_paths(obj):
    """
    Recursively find values that look like BIS PDF/document paths.
    """

    documents = []

    if isinstance(obj, dict):

        for key, value in obj.items():

            if isinstance(value, str):

                value_lower = value.lower()

                if (
                    ".pdf" in value_lower
                    or "bisprod/" in value_lower
                ):
                    documents.append({
                        "field": key,
                        "path": value
                    })

            elif isinstance(value, (dict, list)):

                documents.extend(
                    find_document_paths(value)
                )

    elif isinstance(obj, list):

        for item in obj:

            documents.extend(
                find_document_paths(item)
            )

    return documents


def make_filename(path):
    """
    Convert BIS document path into a safe local filename.
    """

    filename = path.replace("\\", "/").split("/")[-1]

    if not filename:
        filename = "document.pdf"

    return filename


def download_document(path, output_dir):

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    filename = make_filename(path)

    output_path = os.path.join(
        output_dir,
        filename
    )

    # Try each known BIS server
    for base_url in BIS_DOCUMENT_BASE_URLS:

        url = urljoin(
            base_url,
            path.lstrip("/")
        )

        print(f"\nTrying:")
        print(url)

        try:

            response = requests.get(
                url,
                timeout=60,
                headers={
                    "User-Agent":
                        "Mozilla/5.0"
                }
            )

            print(
                f"Status: {response.status_code}"
            )

            if response.status_code == 200:

                content_type = response.headers.get(
                    "Content-Type",
                    ""
                )

                # Save only successful responses
                with open(
                    output_path,
                    "wb"
                ) as f:

                    f.write(
                        response.content
                    )

                print(
                    f"✓ Downloaded: {output_path}"
                )

                return {
                    "source_url": url,
                    "local_path": output_path,
                    "status": "downloaded",
                    "content_type": content_type,
                    "size_bytes": len(
                        response.content
                    )
                }

        except requests.RequestException as e:

            print(
                f"Request failed: {e}"
            )

    print(
        f"✗ Could not download: {path}"
    )

    return {
        "source_path": path,
        "status": "failed"
    }


def download_documents(
    complete_json_path,
    output_dir
):

    print("=" * 70)
    print("BIS DOCUMENT DOWNLOADER")
    print("=" * 70)

    print(
        f"\nReading:\n{complete_json_path}"
    )

    data = load_json(
        complete_json_path
    )

    # ---------------------------------------------------------
    # Find all document references
    # ---------------------------------------------------------

    documents = find_document_paths(
        data
    )

    # Remove duplicates
    unique_documents = {}

    for document in documents:

        path = document["path"]

        unique_documents[path] = document

    documents = list(
        unique_documents.values()
    )

    print(
        f"\nFound {len(documents)} "
        "document references."
    )

    # ---------------------------------------------------------
    # Download
    # ---------------------------------------------------------

    results = []

    for index, document in enumerate(
        documents,
        start=1
    ):

        print("\n" + "-" * 70)

        print(
            f"Document {index}/{len(documents)}"
        )

        print(
            f"Field: {document['field']}"
        )

        print(
            f"Path : {document['path']}"
        )

        result = download_document(
            document["path"],
            output_dir
        )

        result["field"] = document[
            "field"
        ]

        result["source_path"] = document[
            "path"
        ]

        results.append(
            result
        )

    # ---------------------------------------------------------
    # Save download manifest
    # ---------------------------------------------------------

    manifest_path = os.path.join(
        output_dir,
        "download_manifest.json"
    )

    with open(
        manifest_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            results,
            f,
            indent=4,
            ensure_ascii=False
        )

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    successful = sum(
        1
        for result in results
        if result["status"] == "downloaded"
    )

    failed = len(results) - successful

    print("\n" + "=" * 70)
    print("DOWNLOAD COMPLETED")
    print("=" * 70)

    print(
        f"\nSuccessful : {successful}"
    )

    print(
        f"Failed     : {failed}"
    )

    print(
        f"\nManifest:\n{manifest_path}"
    )

    return results