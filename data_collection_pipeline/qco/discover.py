from qco.collector import collect_qco_data


def main():

    print("=" * 70)
    print("BIS QCO COLLECTION PIPELINE")
    print("=" * 70)

    print(
        "\nSTEP 1: Collecting BIS QCO pages..."
    )

    data = collect_qco_data()

    print(
        "\n" + "=" * 70
    )

    print(
        "QCO PIPELINE FINISHED"
    )

    print(
        "=" * 70
    )


if __name__ == "__main__":

    main()