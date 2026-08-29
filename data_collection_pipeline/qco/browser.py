from playwright.sync_api import sync_playwright


BIS_QCO_URL = (
    "https://www.bis.gov.in/"
    "product-certification/"
    "products-under-compulsory-certification/"
    "?lang=en"
)

BIS_UPCOMING_QCO_URL = (
    "https://www.bis.gov.in/"
    "upcoming-qcos-notified-and-due-for-implementation/"
    "?lang=en"
)


def extract_tables(page):

    tables = []

    table_elements = page.locator("table")

    count = table_elements.count()

    for i in range(count):

        table = table_elements.nth(i)

        try:

            rows = table.locator("tr")

            row_count = rows.count()

            extracted_rows = []

            for r in range(row_count):

                cells = rows.nth(r).locator(
                    "th, td"
                )

                cell_count = cells.count()

                row = []

                for c in range(cell_count):

                    value = cells.nth(c).inner_text()

                    value = " ".join(
                        value.split()
                    )

                    row.append(value)

                if row:
                    extracted_rows.append(row)

            if extracted_rows:

                tables.append(
                    extracted_rows
                )

        except Exception:
            continue

    return tables


def discover_qco_requests():

    result = {
        "main_qco_page": {
            "url": BIS_QCO_URL,
            "tables": [],
            "links": []
        },
        "upcoming_qco_page": {
            "url": BIS_UPCOMING_QCO_URL,
            "tables": [],
            "links": []
        }
    }

    print("=" * 70)
    print("BIS QCO DATA COLLECTION")
    print("=" * 70)

    with sync_playwright() as p:

        print("\nLaunching Chromium...")

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        # ====================================================
        # MAIN QCO PAGE
        # ====================================================

        print("\nOpening main QCO page...")

        try:

            page.goto(
                BIS_QCO_URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

        except Exception as e:

            print(
                f"Navigation warning: {e}"
            )

        page.wait_for_timeout(
            10000
        )

        print(
            f"Current URL: {page.url}"
        )

        print(
            f"Title: {page.title()}"
        )

        tables = extract_tables(page)

        result[
            "main_qco_page"
        ][
            "tables"
        ] = tables

        print(
            f"Tables found: {len(tables)}"
        )

        # ----------------------------------------------------
        # Links
        # ----------------------------------------------------

        links = page.locator("a")

        link_count = links.count()

        extracted_links = []

        for i in range(link_count):

            try:

                link = links.nth(i)

                href = link.get_attribute(
                    "href"
                )

                text = " ".join(
                    link.inner_text().split()
                )

                if href:

                    extracted_links.append(
                        {
                            "text": text,
                            "href": href
                        }
                    )

            except Exception:
                continue

        result[
            "main_qco_page"
        ][
            "links"
        ] = extracted_links

        # ====================================================
        # UPCOMING QCO PAGE
        # ====================================================

        print("\nOpening upcoming QCO page...")

        try:

            page.goto(
                BIS_UPCOMING_QCO_URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

        except Exception as e:

            print(
                f"Navigation warning: {e}"
            )

        page.wait_for_timeout(
            10000
        )

        print(
            f"Current URL: {page.url}"
        )

        print(
            f"Title: {page.title()}"
        )

        tables = extract_tables(page)

        result[
            "upcoming_qco_page"
        ][
            "tables"
        ] = tables

        print(
            f"Tables found: {len(tables)}"
        )

        # ----------------------------------------------------
        # Links
        # ----------------------------------------------------

        links = page.locator("a")

        link_count = links.count()

        extracted_links = []

        for i in range(link_count):

            try:

                link = links.nth(i)

                href = link.get_attribute(
                    "href"
                )

                text = " ".join(
                    link.inner_text().split()
                )

                if href:

                    extracted_links.append(
                        {
                            "text": text,
                            "href": href
                        }
                    )

            except Exception:
                continue

        result[
            "upcoming_qco_page"
        ][
            "links"
        ] = extracted_links

        browser.close()

    return result