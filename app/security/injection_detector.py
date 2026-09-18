import re


SUSPICIOUS_PATTERNS = [
    r"ignore (all|any|the|your|previous).*instructions?",
    r"disregard .*instructions?",
    r"forget .*instructions?",
    r"reveal .*system prompt",
    r"show .*system prompt",
    r"print .*system prompt",
    r"what is your system prompt",
    r"developer message",
    r"reveal .*prompt",
    r"bypass .*rules?",
    r"override .*rules?",
    r"ignore .*rules?",
    r"act as .*without restrictions",
    r"jailbreak",

    # Türkçe örnekler
    r"önceki .*talimat.*unut",
    r"önceki .*talimat.*yok say",
    r"talimatları .*görmezden gel",
    r"sistem prompt.*göster",
    r"sistem mesaj.*göster",
    r"gizli .*talimat.*göster",
    r"kuralları .*yok say",
    r"kuralları .*görmezden gel",
]


def detect_prompt_injection(message: str) -> dict:

    normalized = message.lower()

    matched_patterns = []

    for pattern in SUSPICIOUS_PATTERNS:

        if re.search(
            pattern,
            normalized,
            flags=re.IGNORECASE
        ):
            matched_patterns.append(pattern)

    suspicious = len(matched_patterns) > 0

    # Şimdilik basit risk skoru.
    risk_score = min(
        len(matched_patterns) * 40,
        100
    )

    if risk_score >= 80:
        risk_level = "high"
    elif risk_score >= 40:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "suspicious": suspicious,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "matches": matched_patterns
    }