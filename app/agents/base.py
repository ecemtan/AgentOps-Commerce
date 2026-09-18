from typing import Any


def create_agent_result(
    answer: str,
    sources: list[str] | None = None,
    response_type: str = "unknown",
    metadata: dict[str, Any] | None = None
) -> dict:

    return {
        "answer": answer,
        "sources": sources or [],
        "response_type": response_type,
        "metadata": metadata or {}
    }