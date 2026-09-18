from app.security.input_validator import validate_input
from app.security.injection_detector import detect_prompt_injection
from app.security.pii_masker import mask_pii


def analyze_request(message: str) -> dict:

    validation = validate_input(message)

    if not validation["valid"]:
        return {
            "allowed": False,
            "message": "",
            "risk_score": 100,
            "risk_level": "high",
            "pii_detected": False,
            "pii_types": [],
            "security_flags": ["invalid_input"],
            "reason": validation["reason"]
        }

    cleaned_message = validation["cleaned_message"]

    injection = detect_prompt_injection(
        cleaned_message
    )

    pii = mask_pii(
        cleaned_message
    )

    security_flags = []

    if injection["suspicious"]:
        security_flags.append(
            "prompt_injection_suspected"
        )

    if pii["pii_detected"]:
        security_flags.append(
            "pii_detected"
        )

    # v1: Şüpheli injection request'lerini LLM'e göndermiyoruz.
    blocked = injection["risk_level"] in {
        "medium",
        "high"
    }

    return {
        "allowed": not blocked,
        "message": pii["masked_message"],
        "risk_score": injection["risk_score"],
        "risk_level": injection["risk_level"],
        "pii_detected": pii["pii_detected"],
        "pii_types": pii["pii_types"],
        "security_flags": security_flags,
        "reason": (
            "Şüpheli prompt injection tespit edildi."
            if blocked
            else None
        )
    }