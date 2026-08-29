# regulatory/main.py

import os

from regulatory.sources import SOURCES

from regulatory.storage import (
    ensure_directories,
    save_json
)

from regulatory.collector import (
    collect_page,
    download_page_pdfs
)

from regulatory.pressure_cooker import (
    collect_pressure_cooker_qco
)


def main():

    print("=" * 70)
    print(
        "BIS REGULATORY DATA COLLECTION PIPELINE"
    )
    print("=" * 70)

    ensure_directories()

    all_results = []

    # =========================================================
    # 1. QCO PAGES
    # =========================================================

    qco_sources = {

        "qco_main": (
            SOURCES["qco_main"],
            "qco"
        ),

        "qco_upcoming": (
            SOURCES["qco_upcoming"],
            "qco"
        ),

        "qco_scheme_1": (
            SOURCES["qco_scheme_1"],
            "qco"
        ),

        "qco_guidance": (
            SOURCES["qco_guidance"],
            "qco"
        )
    }

    # =========================================================
    # 2. BIS LEGAL FRAMEWORK
    # =========================================================

    legal_sources = {

        "bis_act_rules_regulations": (
            SOURCES[
                "bis_act_rules_regulations"
            ],
            "bis_act"
        )
    }

    # =========================================================
    # 3. CERTIFICATION
    # =========================================================

    certification_sources = {

        "certification_process": (
            SOURCES[
                "certification_process"
            ],
            "certification"
        ),

        "product_certification": (
            SOURCES[
                "product_certification"
            ],
            "certification"
        ),

        "certification_faq": (
            SOURCES[
                "certification_faq"
            ],
            "certification"
        ),

        "certification_archive": (
            SOURCES[
                "certification_archive"
            ],
            "certification"
        )
    }

    # =========================================================
    # 4. PRODUCT MANUAL ARCHIVE
    # =========================================================

    general_sources = {

        "product_manual_archive": (
            SOURCES[
                "product_manual_archive"
            ],
            "general"
        )
    }

    all_sources = {}

    all_sources.update(
        qco_sources
    )

    all_sources.update(
        legal_sources
    )

    all_sources.update(
        certification_sources
    )

    all_sources.update(
        general_sources
    )

    # =========================================================
    # COLLECT
    # =========================================================

    for name, (
        url,
        category
    ) in all_sources.items():

        try:

            result = collect_page(
                name,
                url,
                category
            )

            all_results.append(
                result
            )

            # -------------------------------------------------
            # Download PDFs
            # -------------------------------------------------

            if (
                result.get("status")
                != "failed"
            ):

                print(
                    "\nDownloading discovered PDFs..."
                )

                downloads = (
                    download_page_pdfs(
                        result,
                        category
                    )
                )

                result[
                    "download_results"
                ] = downloads

        except Exception as e:

            print(
                f"\n✗ {name} failed:"
            )

            print(e)

    # =========================================================
    # PRESSURE COOKER QCO
    # =========================================================

    print("\n" + "=" * 70)

    print(
        "VERIFYING PRESSURE COOKER QCO"
    )

    print("=" * 70)

    pressure_cooker_qco = (
        collect_pressure_cooker_qco()
    )

    # =========================================================
    # MASTER MANIFEST
    # =========================================================

    manifest = {

        "source":
            "Bureau of Indian Standards",

        "product":
            "Domestic Pressure Cooker",

        "standard":
            "IS 2347:2023",

        "pages_collected":
            all_results,

        "pressure_cooker_qco":
            pressure_cooker_qco
    }

    manifest_path = (
        "data/raw/regulatory/"
        "regulatory_manifest.json"
    )

    save_json(
        manifest_path,
        manifest
    )

    # =========================================================
    # COMPLETE
    # =========================================================

    print("\n" + "=" * 70)

    print(
        "REGULATORY COLLECTION COMPLETED"
    )

    print("=" * 70)

    print(
        f"\nMaster manifest:"
    )

    print(
        manifest_path
    )

    print(
        "\nSources processed:"
    )

    print(
        len(all_results)
    )


if __name__ == "__main__":

    main()