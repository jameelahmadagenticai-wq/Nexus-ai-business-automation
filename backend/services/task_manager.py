import uuid
import asyncio


# =========================
# Task Storage
# =========================

TASKS = {}

# =========================
# SSE Clients
# =========================

clients = []


# =========================
# Create Task
# =========================

def create_task():

    task_id = str(uuid.uuid4())

    TASKS[task_id] = {
        "status": "pending",
        "result": None
    }

    return task_id


# =========================
# Update Task
# =========================

async def update_task(
    task_id: str,
    status: str,
    result=None
):

    TASKS[task_id] = {
        "status": status,
        "result": result
    }

    # Broadcast to SSE clients
    for queue in clients:
        await queue.put({
            "task_id": task_id,
            "status": status,
            "result": result
        })


# =========================
# Get Task
# =========================

def get_task(task_id: str):

    return TASKS.get(task_id)