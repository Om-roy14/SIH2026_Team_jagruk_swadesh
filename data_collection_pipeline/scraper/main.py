from scraper.collector import collect_bis_page


def main():

    print("=" * 70)
    print(
        "BIS COMPLETE DATA PIPELINE"
    )
    print("=" * 70)

    url = input(
        "\nEnter BIS Standard URL:\n"
    ).strip()

    if not url:

        print(
            "\nError: URL cannot be empty."
        )

        return

    try:

        collect_bis_page(
            url
        )

    except KeyboardInterrupt:

        print(
            "\n\nPipeline interrupted."
        )

    except Exception as e:

        print(
            "\n\nPIPELINE ERROR"
        )

        print(
            str(e)
        )


if __name__ == "__main__":
    main()