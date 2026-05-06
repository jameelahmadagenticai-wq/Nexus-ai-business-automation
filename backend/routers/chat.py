from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from starlette.background import BackgroundTask
from typing import Any, Dict, List, Optional

from memory_client import save_memory
from llm_client import LLMClient


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

# =========================
# LLM CLIENT
# =========================

llm = LLMClient()

# =========================
# REQUEST MODEL
# =========================

class ChatRequest(BaseModel):
    message: Optional[str] = None
    history: Optional[List[Dict[str, Any]]] = None


def clean_history(
    history: Optional[List[Dict[str, Any]]]
):

    clean_messages = []

    for message in history or []:

        role = str(
            message.get("role", "user")
        )

        content = str(
            message.get("content", "")
        )

        if content:

            clean_messages.append({
                "role": role,
                "content": content
            })

    return clean_messages[-8:]

# =========================
# NORMAL CHAT
# =========================

@router.post("/")
async def chat(request: ChatRequest):

    if not request.message:

        return {
            "response": "Error: message is required"
        }

    # =========================
    # GENERATE RESPONSE
    # =========================

    ai_response = await llm.generate(
        prompt=request.message,
        model_type="fast",
        history=clean_history(request.history)
    )

    # =========================
    # SAVE MEMORY
    # =========================

    save_memory(
        user_id="1",
        message=request.message
    )

    # =========================
    # RESPONSE
    # =========================

    return {
        "response": ai_response
    }

# =========================
# STREAM CHAT
# =========================

@router.post("/stream")
async def stream_chat(
    request: ChatRequest
):

    async def generate_stream():

        if not request.message:

            yield "Error: message is required"
            return

        full_response = ""

        async for chunk in llm.stream_generate(
            prompt=request.message,
            model_type="fast",
            history=clean_history(request.history)
        ):

            full_response += chunk

            yield chunk

    return StreamingResponse(
        generate_stream(),
        media_type="text/plain",
        background=BackgroundTask(
            save_memory,
            user_id="1",
            message=request.message
        )
    )
