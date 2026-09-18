import re


EMAIL_PATTERN = (
    r"\b[A-Za-z0-9._%+-]+"
    r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

PHONE_PATTERN = (
    r"(?<!\d)"
    r"(?:\+90[\s.-]?)?"
    r"(?:0[\s.-]?)?"
    r"5\d{2}"
    r"[\s.-]?\d{3}"
    r"[\s.-]?\d{2}"
    r"[\s.-]?\d{2}"
    r"(?!\d)"
)

TCKN_PATTERN = r"(?<!\d)\d{11}(?!\d)"


def mask_pii(message: str) -> dict:

    detected_types = []

    masked_message = message

    if re.search(EMAIL_PATTERN, masked_message):
        detected_types.append("email")
        masked_message = re.sub(
            EMAIL_PATTERN,
            "[EMAIL_REDACTED]",
            masked_message
        )

    if re.search(PHONE_PATTERN, masked_message):
        detected_types.append("phone")
        masked_message = re.sub(
            PHONE_PATTERN,
            "[PHONE_REDACTED]",
            masked_message
        )

    if re.search(TCKN_PATTERN, masked_message):
        detected_types.append("tckn")
        masked_message = re.sub(
            TCKN_PATTERN,
            "[TCKN_REDACTED]",
            masked_message
        )

    return {
        "masked_message": masked_message,
        "pii_detected": bool(detected_types),
        "pii_types": detected_types
    }