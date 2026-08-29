# regulatory/storage.py

import json
import os


BASE_DIR = "data/raw/regulatory"


def ensure_directories():

    directories = [
        BASE_DIR,
        os.path.join(BASE_DIR, "qco"),
        os.path.join(BASE_DIR, "bis_act"),
        os.path.join(BASE_DIR, "regulations"),
        os.path.join(BASE_DIR, "certification"),
        os.path.join(BASE_DIR, "general"),
    ]

    for directory in directories:
        os.makedirs(
            directory,
            exist_ok=True
        )


def save_json(path, data):

    os.makedirs(
        os.path.dirname(path),
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


def save_text(path, text):

    os.makedirs(
        os.path.dirname(path),
        exist_ok=True
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(text)