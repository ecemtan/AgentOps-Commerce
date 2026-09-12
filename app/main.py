from fastapi import FastAPI
from app.api.chat import router as chat_router

app = FastAPI(
    title="AgentOps Commerce",
    description="Multi-agent AI customer support platform",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "service": "AgentOps Commerce",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "AgentOps-Commerce",
        "version": "0.1.0"
    }


app.include_router(chat_router)