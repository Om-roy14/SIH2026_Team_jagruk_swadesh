import json
import os


def save_json(
    path,
    data
):

    directory = os.path.dirname(
        path
    )

    if directory:

        os.makedirs(
            directory,
            exist_ok=True
        )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def save_qco_data(
    data,
    output_dir="data/raw/qco"
):

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Raw discovery data
    # --------------------------------------------------------

    raw_path = os.path.join(
        output_dir,
        "qco_raw.json"
    )

    save_json(
        raw_path,
        data
    )

    # --------------------------------------------------------
    # Structured QCO data
    # --------------------------------------------------------

    structured_path = os.path.join(
        output_dir,
        "qco.json"
    )

    save_json(
        structured_path,
        data
    )

    return {
        "raw": raw_path,
        "structured": structured_path
    }