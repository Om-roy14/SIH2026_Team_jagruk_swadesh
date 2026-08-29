def _convert_response_to_records(data):

    if data is None:
        return []

    # Direct list
    if isinstance(data, list):
        return data

    # Direct dictionary
    if isinstance(data, dict):

        # Common API containers
        possible_keys = [
            "data",
            "records",
            "result",
            "results",
            "response",
            "responseData",
            "items",
            "content",
        ]

        for key in possible_keys:

            value = data.get(key)

            if isinstance(value, list):
                return value

        # The dictionary itself is useful data
        return [data]

    return [
        {
            "value": data
        }
    ]


def collect_endpoint(api):

    endpoint = api["endpoint"]

    url = api["url"]

    responses = api.get(
        "responses",
        []
    )

    all_records = []

    errors = []

    # ---------------------------------------------------------
    # The browser already captured the real BIS responses.
    # Use those responses directly.
    # ---------------------------------------------------------

    for response in responses:

        status = response.get(
            "status"
        )

        data = response.get(
            "data"
        )

        if status is None:
            continue

        if status < 200 or status >= 300:

            errors.append(
                f"HTTP {status}"
            )

            continue

        records = _convert_response_to_records(
            data
        )

        all_records.extend(
            records
        )

    return {
        "endpoint": endpoint,
        "url": url,
        "method": api.get(
            "method"
        ),
        "post_data": api.get(
            "post_data"
        ),
        "records": all_records,
        "responses": responses,
        "error": (
            "; ".join(errors)
            if errors
            else None
        )
    }