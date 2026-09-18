NO_KNOWLEDGE_RESPONSE = (
    "Bu konuda bilgi tabanında yeterli bilgi bulunamadı."
)


def evaluate_escalation(
    answer: str,
    selected_agent: str | None,
    sources: list[str],
    security: dict,
    response_type: str = "unknown"
) -> dict:

    reasons = []

    # RAG cevabı bilgi tabanında bulunamadıysa
    # insan desteğine aktar.
    if answer.strip() == NO_KNOWLEDGE_RESPONSE:
        reasons.append("knowledge_not_found")

    # Hiç agent seçilemediyse.
    if selected_agent is None:
        reasons.append("agent_not_selected")

    # Güvenlik riski varsa.
    if security.get("risk_level") in {
        "medium",
        "high"
    }:
        reasons.append("security_risk")

    # Tool çalışırken hata oluştuysa.
    if response_type == "tool_error":
        reasons.append("tool_error")

    # Deterministic cevapların source'a
    # ihtiyacı yoktur.
    source_required_types = {
        "tool",
        "rag"
    }

    if (
        response_type in source_required_types
        and not sources
        and answer.strip() != NO_KNOWLEDGE_RESPONSE
    ):
        reasons.append("unverified_response")

    return {
        "required": bool(reasons),
        "reasons": reasons
    }