from fastapi import APIRouter
from app.models.chat import ChatRequest
from app.agents.supervisor import route_message

router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest):
    selected_agent = route_message(request.message)

    return {
        "message": request.message,
        "selected_agent": selected_agent
    }