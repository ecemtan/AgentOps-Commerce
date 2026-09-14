from fastapi import APIRouter

from app.models.chat import ChatRequest
from app.agents.supervisor import route_message
from app.agents.order_agent import handle_order
from app.agents.refund_agent import handle_refund
from app.agents.product_agent import handle_product
from app.agents.general_agent import handle_general

router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest):
    selected_agent = route_message(request.message)

    if selected_agent == "order":
        response = handle_order(request.message)

    elif selected_agent == "refund":
        response = handle_refund(request.message)

    elif selected_agent == "product":
        response = handle_product(request.message)

    else:
        response = handle_general(request.message)

    return {
        "message": request.message,
        "selected_agent": selected_agent,
        "response": response
    }