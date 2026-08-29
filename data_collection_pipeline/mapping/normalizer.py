import re


# ============================================================
# STANDARD REGEX
# ============================================================

STANDARD_PATTERN = re.compile(
    r"\bIS\s*\d{1,6}(?::\s*\d{4})?\b",
    re.IGNORECASE
)


# ============================================================
# NORMALIZE STANDARD
# ============================================================

def normalize_standard(value):
    """
    Normalize an Indian Standard number.

    Examples:

        IS2347:2017
        IS 2347:2017
        is 2347:2017
        IS 2347

    become:

        IS 2347:2017
        IS 2347
    """

    if value is None:
        return None

    value = str(value).strip()

    if not value:
        return None

    match = re.search(
        r"\bIS\s*(\d{1,6})(?::\s*(\d{4}))?\b",
        value,
        re.IGNORECASE
    )

    if not match:
        return value

    number = match.group(1)

    year = match.group(2)

    if year:
        return f"IS {number}:{year}"

    return f"IS {number}"


# ============================================================
# EXTRACT STANDARD NUMBERS
# ============================================================

def extract_standard_numbers(text):
    """
    Extract all IS standard numbers from text.
    """

    if not text:
        return []

    found = []

    matches = STANDARD_PATTERN.findall(
        str(text)
    )

    for match in matches:

        normalized = normalize_standard(
            match
        )

        if normalized and normalized not in found:
            found.append(normalized)

    return found