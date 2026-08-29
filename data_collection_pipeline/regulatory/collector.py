# regulatory/collector.py

import os
import re
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from regulatory.storage import (
    save_json,
    save_text
)

from regulatory.downloader import (
    download_file
)


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/151 Safari/537.36"
    )
}


def clean_text(text):

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def collect_page(
    name,
    url,
    category
):

    print("\n" + "=" * 70)
    print(
        f"COLLECTING: {name}"
    )
    print("=" * 70)

    print(
        f"\nURL:\n{url}"
    )

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=60
        )

        print(
            f"HTTP Status: "
            f"{response.status_code}"
        )

        response.raise_for_status()

    except Exception as e:

        print(
            f"✗ Page failed: {e}"
        )

        return {
            "source": name,
            "url": url,
            "status": "failed",
            "error": str(e)
        }

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    page_text = soup.get_text(
        "\n",
        strip=True
    )

    links = []

    pdf_links = []

    for anchor in soup.find_all("a"):

        href = anchor.get(
            "href"
        )

        if not href:
            continue

        absolute_url = urljoin(
            url,
            href
        )

        title = clean_text(
            anchor.get_text(
                " ",
                strip=True
            )
        )

        item = {
            "title": title,
            "url": absolute_url
        }

        links.append(
            item
        )

        if (
            ".pdf" in
            absolute_url.lower()
        ):

            pdf_links.append(
                item
            )

    print(
        f"\nLinks found: "
        f"{len(links)}"
    )

    print(
        f"PDF links: "
        f"{len(pdf_links)}"
    )

    output_dir = os.path.join(
        "data",
        "raw",
        "regulatory",
        category
    )

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    page_record = {

        "source": "BIS",

        "name": name,

        "url": url,

        "category": category,

        "http_status":
            response.status_code,

        "page_text":
            page_text,

        "links":
            links,

        "pdf_links":
            pdf_links
    }

    json_path = os.path.join(
        output_dir,
        f"{name}.json"
    )

    text_path = os.path.join(
        output_dir,
        f"{name}.txt"
    )

    save_json(
        json_path,
        page_record
    )

    save_text(
        text_path,
        page_text
    )

    return page_record


def download_page_pdfs(
    page_record,
    category
):

    pdf_links = page_record.get(
        "pdf_links",
        []
    )

    output_dir = os.path.join(
        "data",
        "raw",
        "regulatory",
        category,
        "documents"
    )

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    results = []

    seen = set()

    for pdf in pdf_links:

        url = pdf["url"]

        if url in seen:
            continue

        seen.add(url)

        result = download_file(
            url,
            output_dir
        )

        result["title"] = pdf[
            "title"
        ]

        results.append(
            result
        )

    return results