from fastapi import APIRouter
from pydantic import BaseModel

from memory_client import (
    delete_memory_by_id,
    list_memories,
    update_memory_by_id
)


router = APIRouter(
    prefix="/memory",
    tags=["Memory"]
)

# =========================
# GET MEMORIES
# =========================

@router.get("/")
async def get_memories():

    memories = list_memories(
        user_id="1",
        limit=20
    )

    return {
        "memories": memories
    }

# =========================
# DELETE MEMORY
# =========================

@router.delete("/{memory_id}")
async def delete_memory(
    memory_id: str
):

    return delete_memory_by_id(
        memory_id
    )

# =========================
# UPDATE MODEL
# =========================

class UpdateMemoryRequest(
    BaseModel
):
    content: str

# =========================
# UPDATE MEMORY
# =========================

@router.put("/{memory_id}")
async def update_memory(
    memory_id: str,
    request: UpdateMemoryRequest
):

    return update_memory_by_id(
        memory_id,
        request.content
    )
