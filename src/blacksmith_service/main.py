from fastapi import Body, FastAPI, HTTPException
from .schemas import MessageRequest, MessageResponse

app = FastAPI(title="Blacksmith Project API")


@app.get("/health")
async def health_check():
    """Health check endpoint for service monitoring."""
    return {"status": "ok", "service": "blacksmith_project"}


@app.post("/api/v1/messages", response_model=MessageResponse)
async def process_message(payload: MessageRequest | None = Body(default=None)):
    """
    Accept a short text message, echo it back with a processed confirmation.

    Empty or missing message -> 400 with a friendly, exact error string,
    per BP-003 acceptance criteria. This includes a request with no body
    at all, not just a body with an empty/missing "message" field.
    """
    if payload is None or not payload.message or not payload.message.strip():
        raise HTTPException(status_code=400, detail="Message is required")

    return MessageResponse(
        message=payload.message,
        status="received",
        processed=True,
    )
