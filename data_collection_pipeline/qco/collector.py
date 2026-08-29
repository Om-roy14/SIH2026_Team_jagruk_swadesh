import json
import os
from datetime import datetime

from playwright.sync_api import sync_playwright


MAIN_QCO_URL = (
    "https://www.bis.gov.in/"
    "product-certification/"
    "products-under-compulsory-certification/"
    "?lang=en"
)

UPCOMING_QCO_URL = (
    "https://www.bis.gov.in/"
    "upcoming-qcos-notified-and-due-for-implementation/"
    "?lang=en"
)


OUTPUT_DIR = os.path.join(
    "data",
    "raw",
    "qco"
)


RAW_FILE = os.path.join(
    OUTPUT_DIR,
    "qco_raw.json"
)


STRUCTURED_FILE = os.path.join(
    OUTPUT_DIR,
    "qco.json"
)


# ============================================================
# CREATE DIRECTORY
# ============================================================

def create_output_directory():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


# ============================================================
# EXTRACT TABLE
# ============================================================

def extract_table(page):

    tables = page.locator("table")

    count = tables.count()

    print(
        f"Tables found: {count}"
    )

    if count == 0:
        return []

    table = tables.nth(0)

    rows = table.locator("tr")

    row_count = rows.count()

    if row_count == 0:
        return []

    headers = []

    first_row = rows.nth(0)

    header_cells = first_row.locator(
        "th"
    )

    if header_cells.count() > 0:

        for i in range(
            header_cells.count()
        ):

            headers.append(
                header_cells.nth(i)
                .inner_text()
                .strip()
            )

        start_index = 1

    else:

        cells = first_row.locator(
            "td"
        )

        for i in range(
            cells.count()
        ):

            headers.append(
                f"column_{i + 1}"
            )

        start_index = 0

    records = []

    for row_index in range(
        start_index,
        row_count
    ):

        row = rows.nth(
            row_index
        )

        cells = row.locator(
            "td"
        )

        cell_count = cells.count()

        if cell_count == 0:
            continue

        values = []

        for cell_index in range(
            cell_count
        ):

            value = (
                cells
                .nth(cell_index)
                .inner_text()
                .strip()
            )

            values.append(
                value
            )

        record = {}

        for index, value in enumerate(
            values
        ):

            if index < len(headers):

                key = headers[index]

            else:

                key = (
                    f"column_{index + 1}"
                )

            record[key] = value

        records.append(
            record
        )

    return records


# ============================================================
# EXTRACT PAGE CONTENT
# ============================================================

def extract_page(page, url, page_name):

    print("\n" + "=" * 70)

    print(
        f"COLLECTING: {page_name}"
    )

    print("=" * 70)

    try:

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

    except Exception as e:

        print(
            f"Navigation warning: {e}"
        )

    print(
        f"Current URL: {page.url}"
    )

    print(
        f"Title: {page.title()}"
    )

    print(
        "Waiting for page..."
    )

    page.wait_for_timeout(
        10000
    )

    # --------------------------------------------------------
    # PAGE TEXT
    # --------------------------------------------------------

    try:

        page_text = (
            page.locator("body")
            .inner_text()
            .strip()
        )

    except Exception:

        page_text = ""

    # --------------------------------------------------------
    # TABLE DATA
    # --------------------------------------------------------

    records = extract_table(
        page
    )

    # --------------------------------------------------------
    # LINKS
    # --------------------------------------------------------

    links = []

    anchors = page.locator(
        "a"
    )

    for index in range(
        anchors.count()
    ):

        anchor = anchors.nth(
            index
        )

        try:

            href = anchor.get_attribute(
                "href"
            )

            text = (
                anchor
                .inner_text()
                .strip()
            )

            if href:

                links.append(
                    {
                        "text": text,
                        "href": href
                    }
                )

        except Exception:
            continue

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    return {

        "page_name": page_name,

        "url": url,

        "title": page.title(),

        "text": page_text,

        "records": records,

        "links": links,

        "collected_at":
            datetime.utcnow()
            .isoformat()
            + "Z"
    }


# ============================================================
# STRUCTURE UPCOMING QCO
# ============================================================

def structure_upcoming(records):

    structured = []

    for record in records:

        normalized = {}

        for key, value in record.items():

            clean_key = (
                key
                .strip()
                .lower()
                .replace(
                    " ",
                    "_"
                )
                .replace(
                    "/",
                    "_"
                )
            )

            normalized[
                clean_key
            ] = value

        structured.append(
            normalized
        )

    return structured


# ============================================================
# STRUCTURE MAIN QCO PAGE
# ============================================================

def structure_main_qco(page_data):

    return {

        "source_url":
            page_data["url"],

        "title":
            page_data["title"],

        "description":
            page_data["text"],

        "links":
            page_data["links"]
    }


# ============================================================
# MAIN COLLECTION
# ============================================================

def collect_qco():

    print("=" * 70)

    print(
        "BIS QCO DATA COLLECTION"
    )

    print("=" * 70)

    create_output_directory()

    with sync_playwright() as p:

        print(
            "\nLaunching Chromium..."
        )

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        # ====================================================
        # MAIN QCO
        # ====================================================

        print(
            "\nOpening main QCO page..."
        )

        main_page = extract_page(
            page,
            MAIN_QCO_URL,
            "products_under_compulsory_certification"
        )

        print(
            f"Main QCO records: "
            f"{len(main_page['records'])}"
        )

        # ====================================================
        # UPCOMING QCO
        # ====================================================

        print(
            "\nOpening upcoming QCO page..."
        )

        upcoming_page = extract_page(
            page,
            UPCOMING_QCO_URL,
            "upcoming_qcos"
        )

        print(
            f"Upcoming QCO records: "
            f"{len(upcoming_page['records'])}"
        )

        browser.close()

    # ========================================================
    # RAW DATA
    # ========================================================

    raw_data = {

        "source": "BIS",

        "collected_at":
            datetime.utcnow()
            .isoformat()
            + "Z",

        "main_qco":
            main_page,

        "upcoming_qco":
            upcoming_page
    }

    with open(
        RAW_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            raw_data,
            file,
            indent=4,
            ensure_ascii=False
        )

    # ========================================================
    # STRUCTURED DATA
    # ========================================================

    structured_data = {

        "source":
            "BIS",

        "collected_at":
            raw_data["collected_at"],

        "main_qco": {

            "source_url":
                MAIN_QCO_URL,

            "description":
                main_page["text"],

            "links":
                main_page["links"]
        },

        "upcoming_qco": {

            "source_url":
                UPCOMING_QCO_URL,

            "records":
                structure_upcoming(
                    upcoming_page["records"]
                )
        }
    }

    with open(
        STRUCTURED_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            structured_data,
            file,
            indent=4,
            ensure_ascii=False
        )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print("\n" + "=" * 70)

    print(
        "QCO COLLECTION COMPLETED"
    )

    print("=" * 70)

    print(
        f"\nMain QCO records     : "
        f"{len(main_page['records'])}"
    )

    print(
        f"Upcoming QCO records : "
        f"{len(upcoming_page['records'])}"
    )

    print(
        f"\nRaw data:"
    )

    print(
        RAW_FILE
    )

    print(
        "\nStructured data:"
    )

    print(
        STRUCTURED_FILE
    )

    return structured_data


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    collect_qco()