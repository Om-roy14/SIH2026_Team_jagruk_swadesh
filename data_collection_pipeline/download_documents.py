import json
import os
import re
from urllib.parse import urlparse


import requests


# ============================================================
# BIS DOCUMENT SERVER
# ============================================================

BASE_URL = "https://standards.bis.gov.in/"


# ============================================================
# SANITIZE FILENAME
# ============================================================

def sanitize_filename(filename):

    filename = str(filename)

    return re.sub(
        r'[<>:"/\\|?*]',
        "_",
        filename
    )


# ============================================================
# FIND DOCUMENT REFERENCES
# ============================================================

def find_document_paths(value):

    found = []

    if isinstance(value, dict):

        for key, item in value.items():

            # ------------------------------------------------
            # String values
            # ------------------------------------------------

            if isinstance(item, str):

                lower_key = key.lower()

                is_document_field = (
                    "file" in lower_key
                    or "document" in lower_key
                    or "path" in lower_key
                    or "migrated" in lower_key
                )

                is_document_file = item.lower().endswith(
                    (
                        ".pdf",
                        ".doc",
                        ".docx",
                        ".xls",
                        ".xlsx"
                    )
                )

                if (
                    is_document_field
                    and is_document_file
                ):

                    found.append(
                        (
                            key,
                            item
                        )
                    )

            # ------------------------------------------------
            # Nested values
            # ------------------------------------------------

            else:

                found.extend(
                    find_document_paths(item)
                )

    elif isinstance(value, list):

        for item in value:

            found.extend(
                find_document_paths(item)
            )

    return found


# ============================================================
# CREATE BIS DOCUMENT URL
# ============================================================

def make_document_url(path):

    path = str(path)

    path = path.replace(
        "\\",
        "/"
    )

    path = path.lstrip(
        "/"
    )

    # Already a complete URL
    if path.startswith(
        "http://"
    ) or path.startswith(
        "https://"
    ):

        return path

    # BIS normally stores paths such as:
    #
    # BisProd/bisProd/oldStandards/...
    #
    # Therefore:
    #
    # https://standards.bis.gov.in/
    # + BisProd/...

    return (
        BASE_URL
        + path
    )


# ============================================================
# DOWNLOAD DOCUMENTS
# ============================================================

def download_documents(
    standard_dir,
    standard_number
):

    # ========================================================
    # LOCATE COMPLETE JSON
    # ========================================================

    complete_path = os.path.join(
        standard_dir,
        "complete.json"
    )

    if not os.path.exists(
        complete_path
    ):

        raise FileNotFoundError(
            f"Missing complete.json:\n"
            f"{complete_path}"
        )

    # ========================================================
    # READ COMPLETE JSON
    # ========================================================

    with open(
        complete_path,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(
            file
        )

    # ========================================================
    # DOCUMENT DIRECTORY
    # ========================================================

    documents_dir = os.path.join(
        standard_dir,
        "documents"
    )

    os.makedirs(
        documents_dir,
        exist_ok=True
    )

    # ========================================================
    # FIND DOCUMENT REFERENCES
    # ========================================================

    references = find_document_paths(
        data
    )

    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    unique = []

    seen = set()

    for field, path in references:

        key = (
            field,
            path
        )

        if key in seen:
            continue

        seen.add(
            key
        )

        unique.append(
            key
        )

    # ========================================================
    # HEADER
    # ========================================================

    print("\n" + "=" * 70)
    print(
        "BIS DOCUMENT DOWNLOADER"
    )
    print("=" * 70)

    print(
        f"\nStandard: {standard_number}"
    )

    print(
        f"Found {len(unique)} "
        f"document references."
    )

    # ========================================================
    # REQUEST SESSION
    # ========================================================

    session = requests.Session()

    session.headers.update(
        {
            "User-Agent":
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/151.0.0.0 "
                "Safari/537.36",

            "Referer":
                "https://standards.bis.gov.in/"
        }
    )

    # ========================================================
    # MANIFEST
    # ========================================================

    manifest = []

    # ========================================================
    # DOWNLOAD EACH DOCUMENT
    # ========================================================

    for index, (
        field,
        path
    ) in enumerate(
        unique,
        start=1
    ):

        print(
            "\n" + "-" * 70
        )

        print(
            f"Document "
            f"{index}/{len(unique)}"
        )

        print(
            f"Field: {field}"
        )

        print(
            f"Path : {path}"
        )

        # ----------------------------------------------------
        # CREATE URL
        # ----------------------------------------------------

        url = make_document_url(
            path
        )

        print(
            f"\nTrying:\n{url}"
        )

        # ----------------------------------------------------
        # DOWNLOAD
        # ----------------------------------------------------

        try:

            response = session.get(
                url,
                timeout=60
            )

            print(
                f"Status: "
                f"{response.status_code}"
            )

            # ------------------------------------------------
            # FAILED HTTP STATUS
            # ------------------------------------------------

            if response.status_code != 200:

                print(
                    "✗ Download failed"
                )

                manifest.append(
                    {
                        "field": field,

                        "source_path": path,

                        "url": url,

                        "status": "failed",

                        "http_status":
                            response.status_code
                    }
                )

                continue

            # ------------------------------------------------
            # DETERMINE FILENAME
            # ------------------------------------------------

            filename = os.path.basename(
                urlparse(
                    url
                ).path
            )

            if not filename:

                filename = (
                    f"document_{index}.pdf"
                )

            filename = sanitize_filename(
                filename
            )

            # ------------------------------------------------
            # OUTPUT PATH
            # ------------------------------------------------

            output_path = os.path.join(
                documents_dir,
                filename
            )

            # ------------------------------------------------
            # SAVE FILE
            # ------------------------------------------------

            with open(
                output_path,
                "wb"
            ) as file:

                file.write(
                    response.content
                )

            print(
                f"✓ Downloaded: "
                f"{output_path}"
            )

            # ------------------------------------------------
            # MANIFEST ENTRY
            # ------------------------------------------------

            manifest.append(
                {
                    "field": field,

                    "source_path": path,

                    "url": url,

                    "filename": filename,

                    "local_path": output_path,

                    "status": "success",

                    "http_status":
                        response.status_code,

                    "size_bytes":
                        len(response.content)
                }
            )

        except Exception as e:

            print(
                f"✗ Error: {e}"
            )

            manifest.append(
                {
                    "field": field,

                    "source_path": path,

                    "url": url,

                    "status": "failed",

                    "error": str(e)
                }
            )

    # ========================================================
    # SAVE MANIFEST
    # ========================================================

    manifest_path = os.path.join(
        documents_dir,
        "download_manifest.json"
    )

    with open(
        manifest_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            manifest,
            file,
            indent=4,
            ensure_ascii=False
        )

    # ========================================================
    # STATISTICS
    # ========================================================

    successful = sum(
        1
        for item in manifest
        if item.get("status")
        == "success"
    )

    failed = sum(
        1
        for item in manifest
        if item.get("status")
        == "failed"
    )

    # ========================================================
    # FINAL OUTPUT
    # ========================================================

    print(
        "\n" + "=" * 70
    )

    print(
        "DOWNLOAD COMPLETED"
    )

    print(
        "=" * 70
    )

    print(
        f"\nSuccessful : "
        f"{successful}"
    )

    print(
        f"Failed     : "
        f"{failed}"
    )

    print(
        f"\nDocuments:\n"
        f"{documents_dir}"
    )

    print(
        f"\nManifest:\n"
        f"{manifest_path}"
    )

    return manifest


# ============================================================
# STANDALONE MODE
# ============================================================

if __name__ == "__main__":

    standard_dir = input(
        "Enter standard directory:\n"
    ).strip()

    standard_number = input(
        "\nEnter standard number:\n"
    ).strip()

    download_documents(
        standard_dir,
        standard_number
    )