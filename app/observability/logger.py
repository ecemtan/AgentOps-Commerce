import json
import logging
from datetime import datetime, timezone
from pathlib import Path


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "agentops.log"


logger = logging.getLogger("agentops")
logger.setLevel(logging.INFO)
logger.propagate = False


if not logger.handlers:

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(message)s"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)


def log_request(
    request_id: str,
    session_id: str,
    selected_agent: str | None,
    sources: list[str],
    security: dict,
    latency_ms: float,
    status: str = "success"
) -> None:

    log_data = {
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),

        "request_id": request_id,
        "session_id": session_id,
        "selected_agent": selected_agent,
        "sources": sources,

        "security": {
            "risk_score": security.get(
                "risk_score", 0
            ),
            "risk_level": security.get(
                "risk_level", "low"
            ),
            "flags": security.get(
                "security_flags", []
            )
        },

        "latency_ms": round(
            latency_ms,
            2
        ),

        "status": status
    }

    logger.info(
        json.dumps(
            log_data,
            ensure_ascii=False
        )
    )