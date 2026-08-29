# regulatory/downloader.py

import os
import re
import requests
from urllib.parse import urljoin, urlparse


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/151 Safari/537.36"
    )
}


def sanitize_filename(filename):

    filename = str(filename)

    filename = re.sub(
        r'[<>:"/\\|?*]',
        "_",
        filename
    )

    filename = filename.strip()

    if not filename:
        filename = "document.pdf"

    return filename


def download_file(
    url,
    output_dir,
    filename=None
):

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    if filename is None:

        parsed = urlparse(url)

        filename = os.path.basename(
            parsed.path
        )

    filename = sanitize_filename(
        filename
    )

    output_path = os.path.join(
        output_dir,
        filename
    )

    if os.path.exists(output_path):

        print(
            f"  ✓ Already exists: {filename}"
        )

        return {
            "status": "already_exists",
            "url": url,
            "local_path": output_path
        }

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=90
        )

        response.raise_for_status()

        content_type = (
            response.headers
            .get("Content-Type", "")
            .lower()
        )

        if (
            "pdf" not in content_type
            and not url.lower().endswith(".pdf")
        ):

            print(
                f"  ⚠ Not obviously PDF: "
                f"{content_type}"
            )

        with open(
            output_path,
            "wb"
        ) as file:

            file.write(
                response.content
            )

        print(
            f"  ✓ Downloaded: {filename}"
        )

        return {
            "status": "success",
            "url": url,
            "local_path": output_path,
            "size": len(response.content)
        }

    except Exception as e:

        print(
            f"  ✗ Download failed: {e}"
        )

        return {
            "status": "failed",
            "url": url,
            "error": str(e)
        }


def make_absolute_url(
    base_url,
    href
):

    return urljoin(
        base_url,
        href
    )