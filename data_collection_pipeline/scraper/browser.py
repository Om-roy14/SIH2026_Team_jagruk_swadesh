from playwright.sync_api import sync_playwright


# These are the BIS standard-detail APIs we actually want.
# getStandardsWithDeptAndCommittee is intentionally excluded because
# it belongs to proposal-service and is not part of the standard
# detail dataset.
RELEVANT_ENDPOINTS = {
    "getWebsiteStandardDetails",
    "getCrossRefDetails",
    "getAmendmentDetails",
    "getGazettedetails",
    "getStandardLicenseDetails",
    "getStandardCRSDetails",
    "getStandardMCSDetails",
    "getStandardLaboratoryDetails",
    "getProductManualDetails",
    "getCorrigendumDetails",
    "getSummaryDetails",
    "getStandardFormatDocumentDetails",
}


def discover_apis(page_url):

    discovered = {}

    print("\nLaunching Chromium...")

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        context = browser.new_context()

        page = context.new_page()

        # ---------------------------------------------------------
        # Capture every request
        # ---------------------------------------------------------

        def request_handler(request):

            url = request.url

            if (
                "standardsadmin.bis.gov.in" not in url
                and "standardsmodule.bis.gov.in" not in url
            ):
                return

            if request.resource_type != "xhr":
                return

            endpoint = url.rstrip("/").split("/")[-1]

            if endpoint not in RELEVANT_ENDPOINTS:
                return

            print(
                f"\nREQUEST [{request.method}]"
            )

            print(url)

            print(
                f"  >>> BIS ENDPOINT: {endpoint}"
            )

        # ---------------------------------------------------------
        # Capture API responses
        # ---------------------------------------------------------

        def response_handler(response):

            url = response.url

            if (
                "standardsadmin.bis.gov.in" not in url
                and "standardsmodule.bis.gov.in" not in url
            ):
                return

            if response.request.resource_type != "xhr":
                return

            endpoint = url.rstrip("/").split("/")[-1]

            if endpoint not in RELEVANT_ENDPOINTS:
                return

            try:
                data = response.json()

            except Exception:
                try:
                    data = response.text()
                except Exception:
                    data = None

            print(
                f"\nRESPONSE: {response.status} {url}"
            )

            # Keep the first response for each endpoint.
            #
            # If the same endpoint is called multiple times,
            # later responses can still be useful, so maintain
            # a response list.
            if endpoint not in discovered:

                discovered[endpoint] = {
                    "endpoint": endpoint,
                    "url": url,
                    "method": response.request.method,
                    "post_data": response.request.post_data,
                    "headers": dict(response.request.headers),
                    "responses": []
                }

            discovered[endpoint]["responses"].append(
                {
                    "status": response.status,
                    "data": data
                }
            )

        page.on(
            "request",
            request_handler
        )

        page.on(
            "response",
            response_handler
        )

        # ---------------------------------------------------------
        # Open BIS page
        # ---------------------------------------------------------

        print("\nOpening BIS page...")

        try:

            page.goto(
                page_url,
                wait_until="commit",
                timeout=60000
            )

        except Exception as e:

            print(
                f"\nPage navigation warning: {e}"
            )

        # ---------------------------------------------------------
        # Give Angular application time to load
        # ---------------------------------------------------------

        print(
            "\nWaiting for BIS application/API calls..."
        )

        page.wait_for_timeout(
            30000
        )

        # ---------------------------------------------------------
        # If nothing appeared, wait longer
        # ---------------------------------------------------------

        if not discovered:

            print(
                "\nNo APIs detected yet."
            )

            print(
                "Waiting another 20 seconds..."
            )

            page.wait_for_timeout(
                20000
            )

        print(
            "\nCurrent page:"
        )

        print(
            page.url
        )

        # ---------------------------------------------------------
        # Final result
        # ---------------------------------------------------------

        print(
            "\nFinal discovered APIs:"
        )

        for endpoint in discovered:

            print(
                f"  ✓ {endpoint}"
            )

        print(
            f"\nTotal: {len(discovered)}"
        )

        browser.close()

    return list(
        discovered.values()
    )