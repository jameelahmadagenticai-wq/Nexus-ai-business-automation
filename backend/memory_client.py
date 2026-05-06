from mem0 import Memory

from cache import (
    build_cache_key,
    cache_response,
    get_cached_response
)


config = {

    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "nexus_memory"
        }
    },

    "llm": {
        "provider": "ollama",
        "config": {
            "model": "llama3"
        }
    },

    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text"
        }
    }
}

_memory_client = None


# =========================
# CLIENT
# =========================

def get_memory_client():

    global _memory_client

    if _memory_client is None:

        _memory_client = Memory.from_config(
            config
        )

    return _memory_client


# =========================
# NORMALIZE
# =========================

def normalize_memories(
    memories
):

    if isinstance(memories, dict):

        memories = (
            memories.get("results")
            or memories.get("memories")
            or memories.get("data")
            or []
        )

    if not isinstance(memories, list):

        return []

    normalized = []

    for memory in memories:

        if isinstance(memory, dict):

            memory_text = (
                memory.get("memory")
                or memory.get("content")
                or memory.get("text")
                or ""
            )

            memory_id = (
                memory.get("id")
                or memory.get("memory_id")
                or memory.get("uuid")
                or ""
            )

            normalized.append({
                **memory,
                "id": str(memory_id),
                "memory": str(memory_text)
            })

        else:

            normalized.append({
                "id": "",
                "memory": str(memory)
            })

    return normalized


# =========================
# SAVE MEMORY
# =========================

def save_memory(
    user_id: str,
    message: str
):

    if not message:

        return True

    try:

        memory_key = build_cache_key(
            "memory",
            user_id,
            message
        )

        if get_cached_response(memory_key):

            return True

        get_memory_client().add(
            message,
            user_id=user_id
        )

        cache_response(
            memory_key,
            "saved"
        )

        return True

    except Exception:

        return False


# =========================
# RETRIEVE MEMORIES
# =========================

def retrieve_memories(
    user_id: str,
    query: str,
    limit: int = 5
):

    try:

        memories = get_memory_client().search(
            query=query,
            filters={
                "user_id": user_id
            },
            limit=limit
        )

        return normalize_memories(
            memories
        )

    except Exception:

        return []


# =========================
# LIST MEMORIES
# =========================

def list_memories(
    user_id: str,
    limit: int = 20
):

    return retrieve_memories(
        user_id=user_id,
        query="user memories",
        limit=limit
    )


# =========================
# DELETE MEMORY
# =========================

def delete_memory_by_id(
    memory_id: str
):

    try:

        get_memory_client().delete(
            memory_id=memory_id
        )

        return {
            "message": "Memory deleted"
        }

    except Exception as exc:

        return {
            "error": str(exc)
        }


# =========================
# UPDATE MEMORY
# =========================

def update_memory_by_id(
    memory_id: str,
    content: str
):

    try:

        get_memory_client().update(
            memory_id=memory_id,
            data=content
        )

        return {
            "message": "Memory updated"
        }

    except Exception as exc:

        return {
            "error": str(exc)
        }
