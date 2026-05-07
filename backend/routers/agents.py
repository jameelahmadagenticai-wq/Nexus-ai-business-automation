import json
import asyncio

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from pydantic import BaseModel

from agents.base.graph import app

from services.task_manager import (
    create_task,
    update_task,
    get_task,
    clients
)


router = APIRouter()


# =========================
# Request Schema
# =========================

class AgentRequest(BaseModel):
    task: str


# =========================
# Run Agent Task
# =========================

@router.post("/run")
async def run_agent_task(
    request: AgentRequest
):

    task_id = create_task()

    asyncio.create_task(
        execute_task(
            task_id,
            request.task
        )
    )

    return {
        "task_id": task_id,
        "status": "started"
    }


# =========================
# Execute Graph Task
# =========================

async def execute_task(
    task_id: str,
    task: str
):

    await update_task(
        task_id,
        "running"
    )

    initial_state = {
        "task": task,
        "agent_name": "",
        "next_agent": "",
        "messages": [],
        "result": "",
        "status": "running"
    }

    result = await app.ainvoke(initial_state)

    await update_task(
        task_id,
        "completed",
        result
    )


# =========================
# Get Task Status
# =========================

@router.get("/{task_id}")
async def get_task_status(
    task_id: str
):

    task = get_task(task_id)

    if not task:
        return {
            "error": "Task not found"
        }

    return task


# =========================
# SSE Stream Endpoint
# =========================

@router.get("/stream/events")
async def stream_events():

    queue = asyncio.Queue()

    clients.append(queue)

    async def event_generator():

        try:

            while True:

                data = await queue.get()

                yield f"data: {json.dumps(data)}\n\n"

        except asyncio.CancelledError:

            if queue in clients:
                clients.remove(queue)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )