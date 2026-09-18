import time
from uuid import uuid4

from fastapi import APIRouter

from app.models.chat import ChatRequest

from app.agents.supervisor import route_message
from app.agents.order_agent import handle_order
from app.agents.refund_agent import handle_refund
from app.agents.product_agent import handle_product
from app.agents.general_agent import handle_general

from app.memory.session_store import (
    enrich_message_with_memory,
    update_session
)

from app.security.security_service import (
    analyze_request
)

from app.observability.logger import (
    log_request
)

from app.escalation.escalation_service import (
    evaluate_escalation
)


router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest):

    start_time = time.perf_counter()
    request_id = str(uuid4())

    # -----------------------------------------
    # 1. SECURITY
    # -----------------------------------------

    security = analyze_request(request.message)

    if not security["allowed"]:

        latency_ms = (
            time.perf_counter() - start_time
        ) * 1000

        log_request(
            request_id=request_id,
            session_id=request.session_id,
            selected_agent=None,
            sources=[],
            security=security,
            latency_ms=latency_ms,
            status="blocked"
        )

        return {
            "request_id": request_id,
            "session_id": request.session_id,
            "message": request.message,
            "selected_agent": None,
            "response": (
                "Bu istek güvenlik politikaları "
                "nedeniyle işlenemedi."
            ),
            "sources": [],

            "security": {
                "risk_score": security["risk_score"],
                "risk_level": security["risk_level"],
                "flags": security["security_flags"]
            },

            "human_escalation": {
                "required": True,
                "reasons": ["security_risk"]
            },

            "latency_ms": round(latency_ms, 2)
        }

    safe_message = security["message"]

    # -----------------------------------------
    # 2. MEMORY
    # -----------------------------------------

    enriched_message = enrich_message_with_memory(
        request.session_id,
        safe_message
    )

    # -----------------------------------------
    # 3. SUPERVISOR
    # -----------------------------------------

    selected_agent = route_message(
        enriched_message
    )

    # -----------------------------------------
    # 4. AGENT
    # -----------------------------------------

    if selected_agent == "order":
        result = handle_order(
            enriched_message
        )

    elif selected_agent == "refund":
        result = handle_refund(
            enriched_message
        )

    elif selected_agent == "product":
        result = handle_product(
            enriched_message
        )

    else:
        result = handle_general(
            enriched_message
        )

    # -----------------------------------------
    # 5. HUMAN ESCALATION
    # -----------------------------------------

    escalation = evaluate_escalation(
    answer=result["answer"],
    selected_agent=selected_agent,
    sources=result["sources"],
    security=security,
    response_type=result.get(
        "response_type",
        "unknown"
    )
)
    # -----------------------------------------
    # 6. MEMORY UPDATE
    # -----------------------------------------

    update_session(
        session_id=request.session_id,
        user_message=safe_message,
        assistant_response=result["answer"]
    )

    # -----------------------------------------
    # 7. OBSERVABILITY
    # -----------------------------------------

    latency_ms = (
        time.perf_counter() - start_time
    ) * 1000

    log_request(
        request_id=request_id,
        session_id=request.session_id,
        selected_agent=selected_agent,
        sources=result["sources"],
        security=security,
        latency_ms=latency_ms
    )

    # -----------------------------------------
    # 8. RESPONSE
    # -----------------------------------------

    return {
        "request_id": request_id,
        "session_id": request.session_id,
        "message": request.message,
        "selected_agent": selected_agent,
  "response": result["answer"],
"sources": result["sources"],
"response_type": result.get(
    "response_type",
    "unknown"
),
"metadata": result.get(
    "metadata",
    {}
),
"security": {
            "risk_score": security["risk_score"],
            "risk_level": security["risk_level"],
            "flags": security["security_flags"],
            "pii_detected": security["pii_detected"],
            "pii_types": security["pii_types"]
        },

        "human_escalation": escalation,

        "latency_ms": round(latency_ms, 2)
    }