# regulatory/pressure_cooker.py

import os

from regulatory.storage import save_json
from regulatory.downloader import download_file


PRESSURE_COOKER_DATA = {

    "product": {
        "name":
            "Domestic Pressure Cooker",

        "standard_number":
            "IS 2347:2023",

        "standard_title":
            "Domestic Pressure Cooker"
    },

    "qco": {

        "title":
            "Domestic Pressure Cooker "
            "(Quality Control) Order, 2020",

        "notification_number":
            "S.O. 294(E)",

        "notification_date":
            "21 January 2020",

        "effective_date":
            "1 August 2020",

        "issuing_department":
            "Department for Promotion "
            "of Industry and Internal Trade",

        "certifying_authority":
            "Bureau of Indian Standards",

        "scheme":
            "Scheme-I",

        "standard_referenced_in_original_qco":
            "IS 2347:2017",

        "latest_standard_clause":
            "The latest version of Indian Standards "
            "including amendments issued thereof, "
            "as notified by the Bureau from time "
            "to time, shall apply."
    },

    "qco_amendments": [

        {

            "title":
                "Domestic Pressure Cooker "
                "(Quality Control) "
                "(Amendment) Order, 2020",

            "notification_number":
                "S.O. 2019(E)",

            "notification_date":
                "23 June 2020",

            "type":
                "QCO amendment"
        }
    ],

    "official_documents": [

        {

            "type":
                "qco",

            "filename":
                "domestic_pressure_cooker_qco_2020.pdf",

            "url":
                "https://bis.gov.in/wp-content/"
                "uploads/2020/01/"
                "Pressure_cooker_QCO.pdf"
        },

        {

            "type":
                "qco_amendment",

            "filename":
                "domestic_pressure_cooker_qco_amendment_2020.pdf",

            "url":
                "https://www.bis.gov.in/wp-content/"
                "uploads/2020/07/"
                "Extension-Order-Pressure-Cooker.pdf"
        }
    ]
}


def collect_pressure_cooker_qco():

    print("\n" + "=" * 70)
    print(
        "PRESSURE COOKER QCO COLLECTION"
    )
    print("=" * 70)

    output_dir = (
        "data/raw/regulatory/qco"
    )

    documents_dir = os.path.join(
        output_dir,
        "pressure_cooker"
    )

    os.makedirs(
        documents_dir,
        exist_ok=True
    )

    manifest = []

    for document in PRESSURE_COOKER_DATA[
        "official_documents"
    ]:

        print(
            f"\nDownloading:"
        )

        print(
            document["filename"]
        )

        result = download_file(
            document["url"],
            documents_dir,
            document["filename"]
        )

        result["type"] = document[
            "type"
        ]

        result["source"] = (
            "BIS"
        )

        manifest.append(
            result
        )

    PRESSURE_COOKER_DATA[
        "download_manifest"
    ] = manifest

    output_path = os.path.join(
        documents_dir,
        "pressure_cooker_qco.json"
    )

    save_json(
        output_path,
        PRESSURE_COOKER_DATA
    )

    print(
        f"\nSaved:\n{output_path}"
    )

    return PRESSURE_COOKER_DATA