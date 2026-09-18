MAX_MESSAGE_LENGTH = 2000


def validate_input(message: str) -> dict:

    if not isinstance(message, str):
        return {
            "valid": False,
            "reason": "Mesaj metin formatında olmalıdır."
        }

    cleaned_message = message.strip()

    if not cleaned_message:
        return {
            "valid": False,
            "reason": "Boş mesaj gönderilemez."
        }

    if len(cleaned_message) > MAX_MESSAGE_LENGTH:
        return {
            "valid": False,
            "reason": (
                f"Mesaj en fazla {MAX_MESSAGE_LENGTH} "
                "karakter olabilir."
            )
        }

    # Null byte gibi kontrol karakterlerini engelle.
    if "\x00" in cleaned_message:
        return {
            "valid": False,
            "reason": "Geçersiz karakter tespit edildi."
        }

    return {
        "valid": True,
        "reason": None,
        "cleaned_message": cleaned_message
    }